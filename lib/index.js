const { addEvent } = require('./events')
const { PREFIX, VERSION } = require('../config')
const path = require('path')
const fs = require('fs')

const commands = []
let pluginsCount = 0

/**
 * Register a bot command
 * @param {Object} options - Command options
 * @param {Function} handler - Command handler function
 */
function bot(options, handler) {
    if (!options.pattern) return
    
    const command = {
        pattern: options.pattern,
        desc: options.desc || 'No description',
        type: options.type || 'misc',
        name: extractCommandName(options.pattern),
        handler,
        dontAddCommandList: options.dontAddCommandList || false,
        isAdmin: options.isAdmin || false
    }
    
    commands.push(command)
    
    // Register event for this command
    addEvent(async (message, client) => {
        if (!message.text) return
        
        const text = message.text.trim()
        if (!text.startsWith(PREFIX)) return
        
        const match = text.match(new RegExp(`^${PREFIX}${options.pattern}`, 'i'))
        if (match) {
            try {
                // Create context object
                const ctx = {
                    commands,
                    PREFIX,
                    VERSION,
                    pluginsCount
                }
                
                await handler(message, match[1] || '', ctx)
            } catch (error) {
                console.error(`Error in command ${command.name}:`, error)
                await message.reply('❌ An error occurred while executing this command.')
            }
        }
    })
}

/**
 * Extract command name from pattern
 * @param {string} pattern - Command pattern
 * @returns {string} - Command name
 */
function extractCommandName(pattern) {
    const match = pattern.match(/^(\w+)/)
    return match ? match[1] : pattern
}

/**
 * Load all plugins from plugins directory
 */
function loadPlugins() {
    const pluginsDir = path.join(__dirname, '../plugins')
    
    if (!fs.existsSync(pluginsDir)) {
        console.log('Plugins directory not found')
        return
    }
    
    const files = fs.readdirSync(pluginsDir).filter(file => file.endsWith('.js'))
    
    files.forEach(file => {
        try {
            const pluginPath = path.join(pluginsDir, file)
            delete require.cache[require.resolve(pluginPath)]
            require(pluginPath)
            pluginsCount++
            console.log(`✅ Loaded plugin: ${file}`)
        } catch (error) {
            console.error(`❌ Error loading plugin ${file}:`, error.message)
        }
    })
    
    console.log(`📦 Loaded ${pluginsCount} plugins`)
}

/**
 * Utility functions
 */
function addSpace(current, total) {
    const maxLength = total.toString().length
    const currentLength = current.toString().length
    return ' '.repeat(maxLength - currentLength)
}

function textToStylist(text, style) {
    switch (style) {
        case 'mono':
            return `\`${text}\``
        case 'bold':
            return `*${text}*`
        case 'italic':
            return `_${text}_`
        default:
            return text
    }
}

function getUptime(format = 'string') {
    const uptime = process.uptime()
    const hours = Math.floor(uptime / 3600)
    const minutes = Math.floor((uptime % 3600) / 60)
    const seconds = Math.floor(uptime % 60)
    
    if (format === 't') {
        return `${hours}h ${minutes}m ${seconds}s`
    }
    
    return { hours, minutes, seconds }
}

function getRam() {
    const used = process.memoryUsage()
    const total = Math.round(used.rss / 1024 / 1024)
    return `${total}MB`
}

function getDate() {
    const now = new Date()
    const time = now.toLocaleTimeString()
    return [now, time]
}

function getPlatform() {
    return process.platform
}

// Language support (basic)
const lang = {
    plugins: {
        menu: {
            help: {
                format: (prefix, name, time, day, date, version, plugins, ram, uptime, platform) => {
                    return `╭────────────────
│ *👋 Hello ${name}!*
│ *🕒 Time:* ${time}
│ *📅 Day:* ${day}
│ *📆 Date:* ${date}
│ *🤖 Version:* ${version}
│ *📦 Plugins:* ${plugins}
│ *💾 RAM:* ${ram}
│ *⏰ Uptime:* ${uptime}
│ *💻 Platform:* ${platform}
│ *🔧 Prefix:* ${prefix}
╰────────────────`
                }
            }
        }
    }
}

// Load plugins on startup
setTimeout(loadPlugins, 1000)

module.exports = {
    bot,
    addSpace,
    textToStylist,
    getUptime,
    getRam,
    getDate,
    getPlatform,
    lang,
    commands
}
