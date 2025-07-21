const { makeWASocket, DisconnectReason, useMultiFileAuthState } = require('baileys');
const { Boom } = require('@hapi/boom');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

async function generateSession() {
    const sessionDir = path.join(__dirname, 'auth_info_session');
    
    // Create session directory if it doesn't exist
    if (!fs.existsSync(sessionDir)) {
        fs.mkdirSync(sessionDir, { recursive: true });
    }
    
    const { state, saveCreds } = await useMultiFileAuthState(sessionDir);
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true, // This will print QR in terminal
        logger: { level: 'silent', child: () => ({ level: 'silent' }) }
    });
    
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            console.log('\n📱 Scan the QR code above with WhatsApp');
            console.log('Go to WhatsApp > Settings > Linked Devices > Link a Device');
        }
        
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error && (lastDisconnect.error instanceof Boom)) ? 
                lastDisconnect.error.output.statusCode !== DisconnectReason.loggedOut : true;
            
            if (shouldReconnect) {
                console.log('🔄 Reconnecting...');
                generateSession();
            } else {
                console.log('❌ Connection closed. You are logged out.');
                process.exit(0);
            }
        } else if (connection === 'open') {
            console.log('✅ Successfully connected to WhatsApp!');
            
            try {
                // Read the credentials file
                const credsPath = path.join(sessionDir, 'creds.json');
                if (fs.existsSync(credsPath)) {
                    const creds = fs.readFileSync(credsPath, 'utf8');
                    const sessionString = `kentech_multibot_${Buffer.from(creds).toString('base64')}`;
                    
                    console.log('\n🔑 Your Session ID:');
                    console.log('=====================================');
                    console.log(sessionString);
                    console.log('=====================================');
                    console.log('\n📝 Copy this session ID to your config.env file');
                    console.log('Replace SESSION_ID=kentech_multibot_sessionid with:');
                    console.log(`SESSION_ID=${sessionString}`);
                    
                    // Save to file as well
                    fs.writeFileSync('session_id.txt', sessionString);
                    console.log('\n💾 Session ID also saved to session_id.txt file');
                }
            } catch (error) {
                console.error('❌ Error reading session data:', error);
            }
            
            // Close the connection
            sock.end();
            process.exit(0);
        }
    });
    
    sock.ev.on('creds.update', saveCreds);
}

console.log('🚀 Starting WhatsApp Session Generator...');
console.log('⏳ Please wait for QR code to appear...\n');

generateSession().catch(error => {
    console.error('❌ Error generating session:', error);
    process.exit(1);
});
