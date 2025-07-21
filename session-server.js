const express = require('express');
const { makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Store active sessions
const activeSessions = new Map();

// Serve the HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'session-generator.html'));
});

// Generate new session
app.post('/api/generate-session', async (req, res) => {
    try {
        const sessionId = Math.random().toString(36).substring(7);
        const sessionDir = path.join(__dirname, 'sessions', sessionId);
        
        // Create session directory
        if (!fs.existsSync(sessionDir)) {
            fs.mkdirSync(sessionDir, { recursive: true });
        }
        
        const { state, saveCreds } = await useMultiFileAuthState(sessionDir);
        
        const sock = makeWASocket({
            auth: state,
            printQRInTerminal: false,
            logger: { level: 'silent', child: () => ({ level: 'silent' }) }
        });
        
        // Store session info
        activeSessions.set(sessionId, {
            socket: sock,
            sessionDir,
            completed: false,
            sessionData: null
        });
        
        let qrCode = null;
        
        sock.ev.on('connection.update', async (update) => {
            const { connection, lastDisconnect, qr } = update;
            
            if (qr) {
                qrCode = qr;
            }
            
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect?.error && (lastDisconnect.error instanceof Boom)) ? 
                    lastDisconnect.error.output.statusCode !== DisconnectReason.loggedOut : true;
                
                if (shouldReconnect) {
                    console.log('Reconnecting...');
                } else {
                    console.log('Connection closed. You are logged out.');
                    // Clean up
                    activeSessions.delete(sessionId);
                    // Remove session directory
                    if (fs.existsSync(sessionDir)) {
                        fs.rmSync(sessionDir, { recursive: true, force: true });
                    }
                }
            } else if (connection === 'open') {
                console.log('Opened connection');
                
                // Generate session string
                const sessionData = fs.readFileSync(path.join(sessionDir, 'creds.json'), 'utf8');
                const sessionString = Buffer.from(sessionData).toString('base64');
                
                // Update session info
                const session = activeSessions.get(sessionId);
                if (session) {
                    session.completed = true;
                    session.sessionData = `kentech_multibot_${sessionString}`;
                }
                
                // Close the socket
                sock.end();
            }
        });
        
        sock.ev.on('creds.update', saveCreds);
        
        // Wait for QR code generation
        let attempts = 0;
        while (!qrCode && attempts < 10) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            attempts++;
        }
        
        if (qrCode) {
            res.json({ success: true, qr: qrCode, sessionId });
        } else {
            res.status(500).json({ error: 'Failed to generate QR code' });
        }
        
    } catch (error) {
        console.error('Error generating session:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Check session status
app.get('/api/check-session/:sessionId', (req, res) => {
    const { sessionId } = req.params;
    const session = activeSessions.get(sessionId);
    
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    if (session.completed && session.sessionData) {
        res.json({ session: session.sessionData });
        
        // Clean up after successful generation
        setTimeout(() => {
            activeSessions.delete(sessionId);
            if (fs.existsSync(session.sessionDir)) {
                fs.rmSync(session.sessionDir, { recursive: true, force: true });
            }
        }, 10000); // Clean up after 10 seconds
    } else {
        res.json({ session: null });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 Session Generator Server running on http://localhost:${PORT}`);
    console.log(`📱 Open http://localhost:${PORT} in your browser to generate session ID`);
});

// Clean up old sessions every 5 minutes
setInterval(() => {
    const now = Date.now();
    for (const [sessionId, session] of activeSessions.entries()) {
        // Remove sessions older than 10 minutes
        if (now - session.createdAt > 10 * 60 * 1000) {
            activeSessions.delete(sessionId);
            if (fs.existsSync(session.sessionDir)) {
                fs.rmSync(session.sessionDir, { recursive: true, force: true });
            }
        }
    }
}, 5 * 60 * 1000);
