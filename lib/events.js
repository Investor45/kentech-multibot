const { getContentType, jidNormalizedUser } = require('baileys')
const { serialize } = require('./serialize')

const events = []

function addEvent(callback) {
    events.push(callback)
}

async function loadMessage(message, client) {
    try {
        const m = await serialize(message, client)
        
        if (!m.message) return
        
        const messageContent = getContentType(m.message)
        if (messageContent && messageContent !== 'senderKeyDistributionMessage') {
            // Execute all registered events
            for (const event of events) {
                try {
                    await event(m, client)
                } catch (error) {
                    console.error('Error in event handler:', error)
                }
            }
        }
    } catch (error) {
        console.error('Error in loadMessage:', error)
    }
}

module.exports = { loadMessage, addEvent }
