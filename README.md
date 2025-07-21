# 🤖 KENTECH MULTIBOT

[![Deploy](https://img.shields.io/badge/Deploy-Now-brightgreen)](https://kentech-session-generator.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-20+-green.svg)](https://nodejs.org)
[![Session Generator](https://img.shields.io/badge/Get%20Session%20ID-Click%20Here-orange)](https://kentech-session-generator.vercel.app)

**KENTECH MULTIBOT** is a powerful and feature-rich WhatsApp bot built with Node.js and Baileys. It supports multiple sessions, customizable responses, and automated task execution for seamless WhatsApp automation.

> 🔑 **Need a Session ID?** Visit: [**KENTECH Session Generator**](https://kentech-session-generator.vercel.app)

## ✨ Features

- 🚀 **Multi-Session Support** – Manage multiple WhatsApp accounts
- 🌐 **Multi-Language Support** – Available in 10+ languages
- 🎨 **Customizable Responses** – Personalize bot behavior
- 🔧 **Easy Deployment** – Multiple hosting options
- 📱 **QR Code Session Generator** – Simple setup process
- 🛡️ **Anti-Link/Anti-Spam** – Advanced group protection
- 🎵 **Media Processing** – Audio, video, and image manipulation
- 📊 **Database Support** – SQLite & PostgreSQL

## 🌍 Supported Languages

Set your preferred language using the `BOT_LANG` variable in `config.env`:

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Spanish | `es` |
| Hindi | `hi` | French | `fr` |
| Arabic | `ar` | Russian | `ru` |
| Bengali | `bn` | Turkish | `tr` |
| Indonesian | `id` | Urdu | `ur` |

## 🚀 Quick Deploy

> 🔑 **First Step**: Get your Session ID at [**KENTECH Session Generator**](https://kentech-session-generator.vercel.app)

### ⚡ VPS Deployment (Fastest)

**One-command deployment for VPS/Server:**

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

**Perfect for:** VPS, Dedicated Servers, Ubuntu/Debian systems  
**Setup time:** 5-10 minutes  
**Docs:** [VPS Quick Deploy Guide](VPS-QUICK-DEPLOY.md)

---

### 1️⃣ Generate Session ID

🔑 **Get your WhatsApp Session ID using Pairing Code:**

**Option A: Pairing Code (Easiest)**
```bash
npm run pairing
```
1. Enter your phone number with country code (e.g., 237670217260)
2. Get 8-digit pairing code
3. Open WhatsApp → Settings → Linked Devices → Link a Device
4. Tap "Link with phone number instead"
5. Enter the 8-digit code
6. Copy your session ID

**Option B: QR Code**
```bash
npm run qr
```
1. Scan QR code with WhatsApp
2. Copy your session ID

📖 **Detailed Guide**: [PAIRING-CODE-GUIDE.md](PAIRING-CODE-GUIDE.md)

> ⚠️ **Important**: Your session ID is like a password - never share it publicly!

### 2️⃣ Deploy on Heroku

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Investor45/kentech-multibot)

### 3️⃣ Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Investor45/kentech-multibot)

### 4️⃣ Deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Investor45/kentech-multibot)

## 🖥️ VPS Deployment

### Quick Installation (Ubuntu/Debian)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

### Manual Installation

#### 1. **Install Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs git ffmpeg -y

# Install Yarn and PM2
sudo npm install -g yarn pm2
```

#### 2. **Clone Repository**

```bash
git clone https://github.com/Investor45/kentech-multibot.git
cd kentech-multibot
yarn install
```

#### 3. **Configure Environment**

```bash
cp config.env.example config.env
nano config.env
```

**Required Variables:**
```env
SESSION_ID=your_session_id_here
PREFIX=.
STICKER_PACKNAME=KENTECH
BOT_LANG=en
SUDO=your_number_here
```

#### 4. **Start the Bot**

```bash
# Start with PM2
npm start

# Or start directly
node index.js
```

## ⚙️ Configuration Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_ID` | WhatsApp session credentials | Required |
| `PREFIX` | Bot command prefix | `.` |
| `BOT_LANG` | Bot language | `en` |
| `SUDO` | Admin phone numbers (comma-separated). Main admin +237670217260 is always included | - |
| `STICKER_PACKNAME` | Sticker pack name | `KENTECH` |
| `MAX_UPLOAD` | Max file upload size (MB) | `20000` |
| `AUTO_STATUS_VIEW` | Auto view status updates | `true` |
| `REJECT_CALL` | Auto reject calls | `false` |

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/Investor45/kentech-multibot.git
cd kentech-multibot

# Install dependencies
yarn install

# Start in development mode
yarn dev
```

### Project Structure

```
kentech-multibot/
├── lib/                 # Core library files
├── plugins/             # Bot plugins/commands
├── lang/               # Language files
├── media/              # Media assets
├── config.env          # Environment configuration
├── index.js           # Main entry point
└── package.json       # Dependencies
```

## 📝 Available Commands

| Command | Description |
|---------|-------------|
| `.ping` | Check bot responsiveness |
| `.help` | Show available commands |
| `.alive` | Bot status information |
| `.menu` | Display command menu |
| `.img <query>` | Search and download images |
| `.sticker` | Convert image/video to sticker |
| `.weather <city>` | Get weather information |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Baileys](https://github.com/WhiskeySockets/Baileys)** - WhatsApp Web API
- All contributors and users of KENTECH MULTIBOT

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Investor45/kentech-multibot/issues)
- **Discord**: [Join our community](https://discord.gg/YOUR_DISCORD)
- **Telegram**: [Support group](https://t.me/kentechnew)

---

<div align="center">
  <h3>🌟 Star this repository if you found it helpful!</h3>
  <h4>Made with ❤️ by KENTECH Team</h4>
</div>
