const { makeWASocket, DisconnectReason, useMultiFileAuthState, fetchLatestBaileysVersion } = require('baileys');
const { Boom } = require('@hapi/boom');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Simple logger to avoid pino dependency issues
const logger = {
    level: 'silent',
    child: () => logger,
    info: () => {},
    error: () => {},
    warn: () => {},
    debug: () => {},
    trace: () => {}
};

// Create readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function question(query) {
    return new Promise(resolve => rl.question(query, resolve));
}

async function generatePairingCode() {
    console.log('🚀 KENTECH MULTIBOT - Pairing Code Generator');
    console.log('===========================================');
    console.log();
    
    // Get phone number from user input or command line
    let phoneNumber = process.argv[2];
    
    if (!phoneNumber) {
        phoneNumber = await question('📱 Enter your WhatsApp phone number (with country code, no + sign): ');
    }
    
    if (!phoneNumber || phoneNumber.length < 10) {
        console.log('❌ Invalid phone number. Please include country code (e.g., 237670217260)');
        rl.close();
        process.exit(1);
    }
    
    console.log(`📞 Generating pairing code for: +${phoneNumber}`);
    console.log('⏳ Please wait...\n');
    
    const sessionDir = path.join(__dirname, 'auth_info_session');
    
    // Create session directory if it doesn't exist
    if (!fs.existsSync(sessionDir)) {
        fs.mkdirSync(sessionDir, { recursive: true });
    }
    
    // Clear existing session
    if (fs.existsSync(sessionDir)) {
        const files = fs.readdirSync(sessionDir);
        for (const file of files) {
            fs.unlinkSync(path.join(sessionDir, file));
        }
    }
    
    const { state, saveCreds } = await useMultiFileAuthState(sessionDir);
    
    // Get latest version info
    let version, isLatest;
    try {
        const versionInfo = await fetchLatestBaileysVersion();
        version = versionInfo.version;
        isLatest = versionInfo.isLatest;
    } catch (error) {
        console.log('⚠️ Could not fetch latest version, using default...');
        version = [2, 3000, 1014901307];
    }
    
    const sock = makeWASocket({
        version,
        logger: logger,
        printQRInTerminal: false,
        auth: state,
        browser: ['KENTECH MULTIBOT', 'Desktop', '1.0.0'],
        connectTimeoutMs: 60000,
        defaultQueryTimeoutMs: 0,
        keepAliveIntervalMs: 10000,
        generateHighQualityLinkPreview: true,
        syncFullHistory: false,
        markOnlineOnConnect: true,
    });
    
async function generatePairingCode(retryCount = 0) {
        console.log('📱 Requesting pairing code...');
        
        try {
            const code = await sock.requestPairingCode(phoneNumber);
            console.log('\n🔑 YOUR PAIRING CODE:');
            console.log('===================');
            console.log(`📲 ${code}`);
            console.log('===================');
            console.log();
            console.log('📝 Instructions:');
            console.log('1. Open WhatsApp on your phone');
            console.log('2. Go to Settings > Linked Devices');
            console.log('3. Tap "Link a Device"');
            console.log('4. Tap "Link with phone number instead"');
            console.log(`5. Enter this code: ${code}`);
            console.log();
            console.log('⏳ Waiting for you to enter the code in WhatsApp...');
            console.log('💡 This may take up to 2 minutes...');
        } catch (error) {
            console.log('❌ Error generating pairing code:', error.message || error);
            
            // Try a different approach if the first fails
            if (error.message && error.message.includes('Connection Closed')) {
                console.log('🔄 Retrying with different configuration...');
                await new Promise(resolve => setTimeout(resolve, 3000));
                
                try {
                    const retryCode = await sock.requestPairingCode(phoneNumber);
                    console.log('\n🔑 YOUR PAIRING CODE (RETRY):');
                    console.log('========================');
                    console.log(`📲 ${retryCode}`);
                    console.log('========================');
                } catch (retryError) {
                    console.log('❌ Retry failed:', retryError.message || retryError);
                    rl.close();
                    process.exit(1);
                }
            } else {
                rl.close();
                process.exit(1);
            }
        }
    }
    
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;
        
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error && (lastDisconnect.error instanceof Boom)) ? 
                lastDisconnect.error.output.statusCode !== DisconnectReason.loggedOut : true;
            
            if (shouldReconnect && lastDisconnect?.error?.output?.statusCode !== DisconnectReason.restartRequired) {
                console.log('🔄 Connection lost, retrying...');
                await new Promise(resolve => setTimeout(resolve, 5000));
                generatePairingCode();
            } else {
                console.log('❌ Connection closed permanently.');
                rl.close();
                process.exit(0);
            }
        } else if (connection === 'open') {
            console.log('✅ Successfully connected to WhatsApp!');
            
            try {
                // Wait a moment for the connection to stabilize
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Read the credentials file
                const credsPath = path.join(sessionDir, 'creds.json');
                if (fs.existsSync(credsPath)) {
                    const creds = fs.readFileSync(credsPath, 'utf8');
                    const sessionString = `kentech_multibot_${Buffer.from(creds).toString('base64')}`;
                    
                    console.log('\n🔑 YOUR SESSION ID:');
                    console.log('=====================================');
                    console.log(sessionString);
                    console.log('=====================================');
                    console.log('\n📝 Next Steps:');
                    console.log('1. Copy the session ID above');
                    console.log('2. Open your config.env file');
                    console.log('3. Replace SESSION_ID=kentech_multibot_sessionid with:');
                    console.log(`   SESSION_ID=${sessionString}`);
                    console.log('4. Save the file and deploy your bot');
                    
                    // Save to file as well
                    fs.writeFileSync('session_id.txt', sessionString);
                    console.log('\n💾 Session ID also saved to session_id.txt file');
                    console.log('\n🚀 Your KENTECH MULTIBOT is ready to deploy!');
                }
            } catch (error) {
                console.error('❌ Error reading session data:', error);
            }
            
            rl.close();
            sock.end();
            process.exit(0);
        } else if (connection === 'connecting') {
            console.log('🔗 Connecting to WhatsApp...');
        }
    });
    
    sock.ev.on('creds.update', saveCreds);
}

// Handle process termination
process.on('SIGINT', () => {
    console.log('\n👋 Pairing code generation cancelled.');
    rl.close();
    process.exit(0);
});

// Start the pairing code generation
generatePairingCode().catch(error => {
    console.error('❌ Error:', error.message);
    rl.close();
    process.exit(1);
});
