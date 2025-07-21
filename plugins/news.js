const { bot, generateList, getJson } = require('../lib/')

bot(
  {
    pattern: 'news ?(.*)',
    desc: 'Get latest news',
    type: 'misc',
  },
  async (message, match) => {
    try {
      if (!match) {
        // Using NewsAPI for general news
        const { articles } = await getJson('https://newsapi.org/v2/top-headlines?country=us&apiKey=demo')
        const list = generateList(
          articles.slice(0, 10).map((article, index) => ({
            _id: `🆔 ${index + 1}\n`,
            text: `🗞${article.title}\n📅${article.publishedAt ? new Date(article.publishedAt).toLocaleDateString() : ''}\n`,
            id: `news ${article.url}`,
          })),
          'Latest News',
          message.jid,
          message.participant,
          message.id
        )

        return await message.send(list.message, {}, list.type)
      }
      if (match.startsWith('http')) {
        return await message.send(`📰 *News Article*\n\n🔗 ${match}`, { quoted: message.data })
      }
    } catch (error) {
      return await message.send('❌ Unable to fetch news at the moment. Please try again later.')
    }
  }
)
