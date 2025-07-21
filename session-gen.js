const { makeWASocket, DisconnectReason, useMultiFileAuthState } = require('baileys');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

async function generateSession() {
    console.log('🚀 KENTECH MULTIBOT Session Generator');
    console.log('⏳ Starting session generation...\n');
    
    const sessionDir = path.join(__dirname, 'auth_info_session');
    
    if (!fs.existsSync(sessionDir)) {
        fs.mkdirSync(sessionDir, { recursive: true });
    }
    
    const { state, saveCreds } = await useMultiFileAuthState(sessionDir);
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        logger: { level: 'silent', child: () => ({ level: 'silent' }) }
    });
    
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            console.log('📱 Scan the QR code above with WhatsApp');
            console.log('Go to: WhatsApp > Settings > Linked Devices > Link a Device\n');
        }
        
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) {
                console.log('🔄 Reconnecting...');
                generateSession();
            } else {
                console.log('❌ Connection closed.');
                process.exit(0);
            }
        } else if (connection === 'open') {
            console.log('✅ Connected to WhatsApp!\n');
            
            try {
                const credsPath = path.join(sessionDir, 'creds.json');
                if (fs.existsSync(credsPath)) {
                    const creds = fs.readFileSync(credsPath, 'utf8');
                    const sessionString = `kentech_multibot_${Buffer.from(creds).toString('base64')}`;
                    
                    console.log('🔑 Your Session ID:');
                    console.log('=' * 50);
                    console.log(sessionString);
                    console.log('=' * 50);
                    console.log('\n📝 Copy this and paste it in your config.env file');
                    console.log('Replace: SESSION_ID=kentech_multibot_sessionid');
                    console.log(`With: SESSION_ID=${sessionString}`);
                    
                    fs.writeFileSync('session_id.txt', sessionString);
                    console.log('\n💾 Session ID saved to session_id.txt');
                }
            } catch (error) {
                console.error('❌ Error:', error.message);
            }
            
            sock.end();
            process.exit(0);
        }
    });
    
    sock.ev.on('creds.update', saveCreds);
}

generateSession().catch(console.error);
