# 🤖 KENTECH MULTIBOT Session Generator

A beautiful and secure WhatsApp session ID generator for KENTECH MULTIBOT.

![KENTECH Session Generator](https://img.shields.io/badge/KENTECH-Session%20Generator-blue?style=for-the-badge&logo=whatsapp)

## ✨ Features

- 🎨 **Beautiful UI** - Modern, responsive design
- 🔒 **Secure** - No data stored on servers
- ⚡ **Fast** - Quick QR code generation
- 📱 **Mobile Friendly** - Works on all devices
- 🚀 **Easy Deploy** - Multiple hosting options

## 🌐 Live Demo

Visit: [KENTECH Session Generator](https://kentech-session-generator.vercel.app)

## 🚀 Quick Deploy

### Deploy to Vercel

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/YOUR_USERNAME/kentech-session-generator)

### Deploy to Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/YOUR_USERNAME/kentech-session-generator)

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/kentech-session-generator)

## 🛠️ Local Development

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kentech-session-generator.git
   cd kentech-session-generator
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser:**
   ```
   http://localhost:8080
   ```

## 📁 Project Structure

```
kentech-session-generator/
├── kentech-session-generator.html    # Main frontend
├── kentech-session-server.js         # Backend API
├── package.json                      # Dependencies
├── vercel.json                       # Vercel config
├── netlify.toml                      # Netlify config
├── Procfile                          # Railway config
└── README.md                         # Documentation
```

## 🔧 API Endpoints

### `POST /api/generate-session`
Generate a new WhatsApp session

**Response:**
```json
{
  "success": true,
  "qr": "qr_code_data",
  "sessionId": "unique_session_id"
}
```

### `GET /api/check-session/:sessionId`
Check session generation status

**Response:**
```json
{
  "session": "kentech_multibot_base64_session_data",
  "message": "Session generated successfully"
}
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "KENTECH MULTIBOT Session Generator",
  "timestamp": "2025-07-21T00:00:00.000Z"
}
```

## 🔒 Security Features

- ✅ **No data persistence** - Sessions are temporary
- ✅ **Automatic cleanup** - Sessions expire after 5 minutes
- ✅ **Input validation** - All inputs are validated
- ✅ **Error handling** - Proper error responses
- ✅ **Rate limiting** - Prevents abuse (when deployed)

## 🌍 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8080` |
| `NODE_ENV` | Environment | `development` |

## 🎨 Customization

### Changing Colors

Edit the CSS variables in `kentech-session-generator.html`:

```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --accent-color: #FFD700;
  --success-color: #4CAF50;
}
```

### Adding Your Logo

Replace the emoji in the header:

```html
<div class="logo">🤖</div>
<!-- Replace with -->
<div class="logo"><img src="your-logo.png" alt="Logo"></div>
```

## 📝 Usage Instructions

1. **Generate Session ID:**
   - Visit the session generator website
   - Click "Generate QR Code"
   - Scan with WhatsApp
   - Copy the generated session ID

2. **Use in Bot:**
   ```env
   SESSION_ID=kentech_multibot_your_generated_session_here
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Baileys](https://github.com/WhiskeySockets/Baileys)** - WhatsApp Web API
- **[QRCode.js](https://github.com/davidshimjs/qrcodejs)** - QR code generation
- **KENTECH Team** - For the amazing design

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/YOUR_USERNAME/kentech-session-generator/issues)
- **Documentation**: [KENTECH MULTIBOT Docs](https://github.com/YOUR_USERNAME/kentech-multibot)

---

<div align="center">
  <h3>🌟 Star this repository if you found it helpful!</h3>
  <p>Made with ❤️ by KENTECH Team</p>
</div>
