const { mediafire, bot, isUrl } = require('../lib')

bot(
  {
    pattern: 'mediafire ?(.*)',
    desc: 'Download mediafire file',
    type: 'download',
  },
  async (message, match) => {
    match = isUrl(match || message.reply_message.text)
    if (!match) return await message.send('_Example : mediafire url_')
    const result = await mediafire(match)
    if (!result)
      return await message.send('*Not found*', {
        quoted: message.quoted,
      })
    
    const caption = `📁 *Downloaded by KENTECH MULTIBOT*\n\n🔗 *Source:* MediaFire\n📱 *Bot:* KENTECH MULTIBOT\n⚡ *Powered by:* KENTECH Team\n\n_File downloaded successfully! 📥_`
    return await message.sendFromUrl(result, { caption })
  }
)
