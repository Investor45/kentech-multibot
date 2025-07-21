const { bot } = require('../lib/')
const { VERSION } = require('../config')

bot(
  {
    pattern: 'alive ?(.*)',
    desc: 'Check if bot is alive',
    type: 'misc',
  },
  async (message, match) => {
    const uptime = process.uptime()
    const hours = Math.floor(uptime / 3600)
    const minutes = Math.floor((uptime % 3600) / 60)
    const seconds = Math.floor(uptime % 60)
    
    const aliveMessage = `🤖 *KENTECH MULTIBOT IS ALIVE!*

🔥 *Status:* Online & Active
⚡ *Version:* ${VERSION || '1.0.0'}
⏰ *Uptime:* ${hours}h ${minutes}m ${seconds}s
📱 *Bot Name:* KENTECH MULTIBOT
👨‍💻 *Developer:* KENTECH Team
🌐 *Language:* JavaScript (Node.js)

🚀 *Features:*
• Multi-Platform Downloads
• Advanced Media Processing  
• Group Management Tools
• Anti-Link/Anti-Spam Protection
• Multi-Language Support

💬 *Commands:* Send .menu for command list
🔗 *Repository:* github.com/Investor45/kentech-multibot
📞 *Support:* t.me/kentechnew

_Powered by KENTECH Team 🚀_`

    await message.send(aliveMessage, { quoted: message.data })
  }
)
