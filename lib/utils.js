const axios = require('axios')
const fs = require('fs')
const path = require('path')

/**
 * Get buffer from URL or file path
 * @param {string} url - URL or file path
 * @returns {Promise<Buffer>}
 */
async function getBuffer(url) {
    try {
        if (fs.existsSync(url)) {
            return fs.readFileSync(url)
        }
        
        const response = await axios.get(url, {
            responseType: 'arraybuffer',
            timeout: 30000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        })
        
        return Buffer.from(response.data)
    } catch (error) {
        console.error('Error getting buffer:', error.message)
        throw error
    }
}

/**
 * Download file from URL
 * @param {string} url - URL to download
 * @param {string} filename - Optional filename
 * @returns {Promise<string>} - File path
 */
async function downloadFile(url, filename) {
    try {
        const buffer = await getBuffer(url)
        const filePath = path.join(__dirname, '../media', filename || `download_${Date.now()}`)
        
        // Create media directory if it doesn't exist
        const mediaDir = path.dirname(filePath)
        if (!fs.existsSync(mediaDir)) {
            fs.mkdirSync(mediaDir, { recursive: true })
        }
        
        fs.writeFileSync(filePath, buffer)
        return filePath
    } catch (error) {
        console.error('Error downloading file:', error.message)
        throw error
    }
}

/**
 * Check if URL is valid
 * @param {string} url - URL to validate
 * @returns {boolean}
 */
function isUrl(url) {
    try {
        new URL(url)
        return true
    } catch {
        return false
    }
}

/**
 * Format time
 * @param {number} seconds - Time in seconds
 * @returns {string} - Formatted time
 */
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = Math.floor(seconds % 60)
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`
}

/**
 * Format file size
 * @param {number} bytes - Size in bytes
 * @returns {string} - Formatted size
 */
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Sleep function
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise}
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Parse mentions from text
 * @param {string} text - Text to parse
 * @returns {Array} - Array of mentioned JIDs
 */
function parseMentions(text) {
    const mentions = []
    const regex = /@(\d+)/g
    let match
    
    while ((match = regex.exec(text)) !== null) {
        mentions.push(match[1] + '@s.whatsapp.net')
    }
    
    return mentions
}

/**
 * Clean text by removing special characters
 * @param {string} text - Text to clean
 * @returns {string} - Cleaned text
 */
function cleanText(text) {
    return text.replace(/[^\w\s]/gi, '').trim()
}

/**
 * Generate random string
 * @param {number} length - Length of string
 * @returns {string} - Random string
 */
function randomString(length = 10) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    let result = ''
    
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    
    return result
}

module.exports = {
    getBuffer,
    downloadFile,
    isUrl,
    formatTime,
    formatBytes,
    sleep,
    parseMentions,
    cleanText,
    randomString
}
