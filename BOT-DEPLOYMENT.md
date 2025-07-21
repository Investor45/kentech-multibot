# 🤖 KENTECH MULTIBOT - Main Bot Deployment

## 🎯 Deployment Options

### 🌐 **Option 1: Heroku (Recommended for Beginners)**

#### Prerequisites:
- Heroku account
- Valid session ID from session generator

#### Steps:
1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create kentech-multibot-yourname
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SESSION_ID=your_real_session_id_here
   heroku config:set PREFIX=.
   heroku config:set BOT_LANG=en
   heroku config:set STICKER_PACKNAME=KENTECH
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy KENTECH MULTIBOT"
   git push heroku main
   ```

---

### 🚀 **Option 2: Railway (Modern & Fast)**

#### Steps:
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Create new project from GitHub repo
4. Add environment variables:
   - `SESSION_ID`: Your real session ID
   - `PREFIX`: .
   - `BOT_LANG`: en
5. Deploy automatically

---

### 🔧 **Option 3: VPS Deployment (Advanced)**

#### Prerequisites:
- VPS with Ubuntu 20.04+
- Root or sudo access
- Domain name (optional)

#### Auto-Deploy Script:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/kentech-multibot/main/deploy.sh)
```

#### Manual VPS Setup:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2
sudo npm install -g pm2

# Clone repository
git clone https://github.com/YOUR_USERNAME/kentech-multibot.git
cd kentech-multibot

# Install dependencies
npm install

# Configure environment
cp config.env.example config.env
nano config.env  # Add your session ID

# Start with PM2
pm2 start index.js --name "kentech-multibot"
pm2 startup
pm2 save
```

---

### 🐳 **Option 4: Docker Deployment**

#### Using Docker:
```bash
# Build image
docker build -t kentech-multibot .

# Run container
docker run -d \
  --name kentech-multibot \
  -e SESSION_ID=your_session_id \
  -e PREFIX=. \
  -e BOT_LANG=en \
  kentech-multibot
```

#### Using Docker Compose:
```yaml
version: '3.8'
services:
  kentech-multibot:
    build: .
    environment:
      - SESSION_ID=your_session_id_here
      - PREFIX=.
      - BOT_LANG=en
    restart: unless-stopped
```

---

## 🔧 **Environment Variables Guide**

### **Required:**
```env
SESSION_ID=your_real_session_id_from_generator
PREFIX=.
BOT_LANG=en
```

### **Optional:**
```env
STICKER_PACKNAME=KENTECH
ALWAYS_ONLINE=false
AUTO_STATUS_VIEW=true
WARN_LIMIT=3
RMBG_KEY=your_remove_bg_api_key
SUDO=your_phone_number
```

---

## 🧪 **Testing Your Deployment**

1. **Check if bot is online:**
   - Send `.ping` command
   - Bot should respond with latency

2. **Test basic commands:**
   - `.help` - Show all commands
   - `.alive` - Bot status
   - `.ping` - Response test

3. **Test advanced features:**
   - Send an image with `.sticker`
   - Try `.weather your_city`
   - Use `.tts hello world`

---

## 🐛 **Troubleshooting**

### **Bot won't start:**
1. Check session ID is valid (not placeholder)
2. Verify all environment variables
3. Check logs for specific errors
4. Regenerate session ID if needed

### **Commands not working:**
1. Check prefix in config
2. Verify bot permissions in group
3. Check if bot is actually connected
4. Try private message first

### **Session expired:**
1. Generate new session ID
2. Update environment variables
3. Restart the bot
4. Re-add to groups if needed

---

## 📊 **Monitoring & Maintenance**

### **Heroku:**
```bash
heroku logs --tail  # View live logs
heroku restart      # Restart bot
```

### **VPS with PM2:**
```bash
pm2 status          # Check status
pm2 logs            # View logs
pm2 restart all     # Restart bot
```

### **Docker:**
```bash
docker logs kentech-multibot  # View logs
docker restart kentech-multibot  # Restart
```

---

✅ **Your KENTECH MULTIBOT is now deployed and ready for users!**
