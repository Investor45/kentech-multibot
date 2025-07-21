const express = require('express');
const { makeWASocket, DisconnectReason, useMultiFileAuthState } = require('baileys');
const { Boom } = require('@hapi/boom');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Store active sessions
const activeSessions = new Map();

// Serve the main HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'kentech-session-generator.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        service: 'KENTECH MULTIBOT Session Generator',
        timestamp: new Date().toISOString(),
        activeSessions: activeSessions.size
    });
});

// Generate new session
app.post('/api/generate-session', async (req, res) => {
    try {
        const sessionId = uuidv4();
        const sessionDir = path.join(__dirname, 'temp_sessions', sessionId);
        
        // Create session directory
        if (!fs.existsSync(sessionDir)) {
            fs.mkdirSync(sessionDir, { recursive: true });
        }
        
        const { state, saveCreds } = await useMultiFileAuthState(sessionDir);
        
        const sock = makeWASocket({
            auth: state,
            printQRInTerminal: false,
            logger: { 
                level: 'silent',
                child: () => ({ level: 'silent' })
            }
        });
        
        // Store session info with timestamp
        activeSessions.set(sessionId, {
            socket: sock,
            sessionDir,
            completed: false,
            sessionData: null,
            createdAt: Date.now(),
            qrCode: null
        });
        
        let qrCode = null;
        let qrGenerated = false;
        
        sock.ev.on('connection.update', async (update) => {
            const { connection, lastDisconnect, qr } = update;
            
            if (qr && !qrGenerated) {
                qrCode = qr;
                qrGenerated = true;
                const session = activeSessions.get(sessionId);
                if (session) {
                    session.qrCode = qr;
                }
            }
            
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect?.error && (lastDisconnect.error instanceof Boom)) ? 
                    lastDisconnect.error.output.statusCode !== DisconnectReason.loggedOut : false;
                
                if (!shouldReconnect) {
                    console.log(`Session ${sessionId} connection closed`);
                    // Clean up
                    const session = activeSessions.get(sessionId);
                    if (session && !session.completed) {
                        activeSessions.delete(sessionId);
                        // Remove session directory
                        if (fs.existsSync(sessionDir)) {
                            fs.rmSync(sessionDir, { recursive: true, force: true });
                        }
                    }
                }
            } else if (connection === 'open') {
                console.log(`Session ${sessionId} connected successfully`);
                
                try {
                    // Generate session string
                    const credsPath = path.join(sessionDir, 'creds.json');
                    if (fs.existsSync(credsPath)) {
                        const sessionData = fs.readFileSync(credsPath, 'utf8');
                        const sessionString = `kentech_multibot_${Buffer.from(sessionData).toString('base64')}`;
                        
                        // Update session info
                        const session = activeSessions.get(sessionId);
                        if (session) {
                            session.completed = true;
                            session.sessionData = sessionString;
                        }
                        
                        console.log(`Session ${sessionId} generated successfully`);
                    }
                } catch (error) {
                    console.error(`Error processing session ${sessionId}:`, error);
                }
                
                // Close the socket after a short delay
                setTimeout(() => {
                    try {
                        sock.end();
                    } catch (error) {
                        console.error('Error closing socket:', error);
                    }
                }, 2000);
            }
        });
        
        sock.ev.on('creds.update', saveCreds);
        
        // Wait for QR code generation with timeout
        let attempts = 0;
        while (!qrCode && attempts < 15) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            attempts++;
            
            const session = activeSessions.get(sessionId);
            if (session && session.qrCode) {
                qrCode = session.qrCode;
                break;
            }
        }
        
        if (qrCode) {
            res.json({ 
                success: true, 
                qr: qrCode, 
                sessionId,
                message: 'QR code generated successfully'
            });
        } else {
            // Clean up failed session
            activeSessions.delete(sessionId);
            if (fs.existsSync(sessionDir)) {
                fs.rmSync(sessionDir, { recursive: true, force: true });
            }
            res.status(500).json({ 
                error: 'Failed to generate QR code',
                message: 'Please try again'
            });
        }
        
    } catch (error) {
        console.error('Error generating session:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: 'Failed to initialize session generator'
        });
    }
});

// Check session status
app.get('/api/check-session/:sessionId', (req, res) => {
    const { sessionId } = req.params;
    const session = activeSessions.get(sessionId);
    
    if (!session) {
        return res.status(404).json({ 
            error: 'Session not found',
            message: 'Session may have expired or been cleaned up'
        });
    }
    
    if (session.completed && session.sessionData) {
        const sessionData = session.sessionData;
        
        // Schedule cleanup
        setTimeout(() => {
            activeSessions.delete(sessionId);
            if (fs.existsSync(session.sessionDir)) {
                fs.rmSync(session.sessionDir, { recursive: true, force: true });
            }
        }, 30000); // Clean up after 30 seconds
        
        res.json({ 
            session: sessionData,
            message: 'Session generated successfully'
        });
    } else {
        res.json({ 
            session: null,
            status: 'pending',
            message: 'Waiting for WhatsApp connection'
        });
    }
});

// Get session QR code
app.get('/api/session-qr/:sessionId', (req, res) => {
    const { sessionId } = req.params;
    const session = activeSessions.get(sessionId);
    
    if (!session) {
        return res.status(404).json({ 
            error: 'Session not found'
        });
    }
    
    if (session.qrCode) {
        res.json({ 
            qr: session.qrCode,
            message: 'QR code available'
        });
    } else {
        res.json({ 
            qr: null,
            message: 'QR code not yet available'
        });
    }
});

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        error: 'Internal server error',
        message: 'Something went wrong'
    });
});

// Clean up old sessions every 5 minutes
setInterval(() => {
    const now = Date.now();
    const fiveMinutes = 5 * 60 * 1000;
    
    for (const [sessionId, session] of activeSessions.entries()) {
        if (now - session.createdAt > fiveMinutes) {
            console.log(`Cleaning up expired session: ${sessionId}`);
            
            try {
                if (session.socket && session.socket.end) {
                    session.socket.end();
                }
            } catch (error) {
                console.error('Error closing socket during cleanup:', error);
            }
            
            activeSessions.delete(sessionId);
            
            if (fs.existsSync(session.sessionDir)) {
                fs.rmSync(session.sessionDir, { recursive: true, force: true });
            }
        }
    }
}, 5 * 60 * 1000);

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, cleaning up sessions...');
    
    for (const [sessionId, session] of activeSessions.entries()) {
        try {
            if (session.socket && session.socket.end) {
                session.socket.end();
            }
            if (fs.existsSync(session.sessionDir)) {
                fs.rmSync(session.sessionDir, { recursive: true, force: true });
            }
        } catch (error) {
            console.error(`Error cleaning up session ${sessionId}:`, error);
        }
    }
    
    process.exit(0);
});

app.listen(PORT, () => {
    console.log(`🚀 KENTECH MULTIBOT Session Generator running on port ${PORT}`);
    console.log(`📱 Visit http://localhost:${PORT} to generate session IDs`);
    console.log(`🌐 Health check: http://localhost:${PORT}/health`);
});
