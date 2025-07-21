const { default: makeWASocket, DisconnectReason, fetchLatestBaileysVersion, useMultiFileAuthState } = require('baileys')
const { Boom } = require('@hapi/boom')
const pino = require('pino')
const { existsSync, mkdirSync } = require('fs')
const path = require('path')
const { SESSION_ID } = require('../config')
const { getBuffer } = require('./utils')
const { loadMessage } = require('./events')
const { writeFile, readFile } = require('fs/promises')

const logger = pino({ level: 'silent' })

class Client {
    constructor() {
        this.client = null
        this.connected = false
    }

    async connect() {
        const sessionDir = path.join(__dirname, '../auth_info_session')
        
        if (!existsSync(sessionDir)) {
            mkdirSync(sessionDir, { recursive: true })
        }

        // Decode session if provided
        if (SESSION_ID && SESSION_ID.includes('kentech_multibot_')) {
            try {
                const sessionData = SESSION_ID.replace('kentech_multibot_', '')
                const decodedCreds = Buffer.from(sessionData, 'base64').toString('utf-8')
                const credsPath = path.join(sessionDir, 'creds.json')
                await writeFile(credsPath, decodedCreds)
                logger.info('Session loaded from SESSION_ID')
            } catch (error) {
                logger.error('Failed to decode session:', error)
            }
        }

        const { state, saveCreds } = await useMultiFileAuthState(sessionDir)
        const { version } = await fetchLatestBaileysVersion()

        this.client = makeWASocket({
            version,
            logger,
            auth: state,
            browser: ['KENTECH MULTIBOT', 'Chrome', '1.0.0'],
            printQRInTerminal: false,
            defaultQueryTimeoutMs: 60000,
            generateHighQualityLinkPreview: true,
        })

        this.client.ev.on('connection.update', this.connectionUpdate.bind(this))
        this.client.ev.on('creds.update', saveCreds)
        this.client.ev.on('messages.upsert', this.messageHandler.bind(this))

        return this.client
    }

    async connectionUpdate(update) {
        const { connection, lastDisconnect } = update
        
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error instanceof Boom) 
                ? lastDisconnect.error.output.statusCode !== DisconnectReason.loggedOut
                : true

            logger.info('Connection closed due to:', lastDisconnect?.error)
            
            if (shouldReconnect) {
                logger.info('Reconnecting...')
                setTimeout(() => this.connect(), 3000)
            } else {
                logger.info('Bot logged out')
                process.exit(0)
            }
        } else if (connection === 'open') {
            this.connected = true
            logger.info('✅ KENTECH MULTIBOT connected successfully!')
            
            // Send alive message if configured
            const { ALWAYS_ONLINE } = require('../config')
            if (ALWAYS_ONLINE === 'true') {
                setInterval(async () => {
                    try {
                        await this.client.sendPresenceUpdate('available')
                    } catch (error) {
                        logger.error('Presence update error:', error)
                    }
                }, 60000)
            }
        } else if (connection === 'connecting') {
            logger.info('🔗 Connecting to WhatsApp...')
        }
    }

    async messageHandler(m) {
        try {
            if (m.type !== 'notify') return
            for (const message of m.messages) {
                await loadMessage(message, this.client)
            }
        } catch (error) {
            logger.error('Message handler error:', error)
        }
    }

    async sendMessage(jid, content, options = {}) {
        try {
            return await this.client.sendMessage(jid, content, options)
        } catch (error) {
            logger.error('Send message error:', error)
            throw error
        }
    }

    async getProfilePicture(jid) {
        try {
            const url = await this.client.profilePictureUrl(jid, 'image')
            return await getBuffer(url)
        } catch {
            return null
        }
    }
}

module.exports = { Client, logger }