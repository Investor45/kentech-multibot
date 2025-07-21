const { getContentType, jidNormalizedUser, extractMessageContent, downloadMediaMessage } = require('baileys')

function serialize(message, client) {
    if (message.key) {
        message.id = message.key.id
        message.isSelf = message.key.fromMe
        message.from = message.key.remoteJid
        message.isGroup = message.from.endsWith('@g.us')
        message.sender = message.key.fromMe ? client.user.id : message.isGroup ? message.key.participant : message.from
    }

    if (message.message) {
        message.type = getContentType(message.message)
        message.text = message.message.conversation || 
                      message.message.extendedTextMessage?.text || 
                      message.message.imageMessage?.caption || 
                      message.message.videoMessage?.caption || 
                      message.message.documentMessage?.caption || ''
        
        message.quoted = message.message.extendedTextMessage?.contextInfo?.quotedMessage
        
        if (message.quoted) {
            message.quoted.type = getContentType(message.quoted)
            message.quoted.text = message.quoted.conversation || 
                                 message.quoted.extendedTextMessage?.text || 
                                 message.quoted.imageMessage?.caption || 
                                 message.quoted.videoMessage?.caption || ''
        }
    }

    message.reply = async (text, options = {}) => {
        return await client.sendMessage(message.from, { text }, { 
            quoted: message,
            ...options 
        })
    }

    message.download = async () => {
        if (!message.message) return null
        
        const messageType = getContentType(message.message)
        const messageContent = extractMessageContent(message.message)
        
        if (!messageContent || !['imageMessage', 'videoMessage', 'audioMessage', 'documentMessage', 'stickerMessage'].includes(messageType)) {
            return null
        }
        
        try {
            return await downloadMediaMessage(message, 'buffer', {}, {
                logger: { level: 'silent', child: () => ({ level: 'silent' }) },
                reuploadRequest: client.updateMediaMessage
            })
        } catch (error) {
            console.error('Error downloading media:', error)
            return null
        }
    }

    message.react = async (emoji) => {
        return await client.sendMessage(message.from, {
            react: {
                text: emoji,
                key: message.key
            }
        })
    }

    // Normalize JID
    message.jid = jidNormalizedUser(message.from)
    if (message.sender) {
        message.sender = jidNormalizedUser(message.sender)
    }

    return message
}

module.exports = { serialize }
