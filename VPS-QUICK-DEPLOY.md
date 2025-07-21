# 🚀 KENTECH MULTIBOT - VPS Quick Deploy Guide

## ⚡ One-Command VPS Deployment

**Run this single command on your VPS:**

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

**What happens automatically:**
1. ✅ **Downloads and installs** all dependencies (Node.js, Yarn, PM2, Git, FFmpeg)
2. ✅ **Clones your repository** automatically from GitHub
3. ✅ **Asks for your phone number** (e.g., 237670217260)
4. ✅ **Generates 8-digit pairing code** automatically
5. ✅ **You enter code in WhatsApp** (Settings > Linked Devices > Link with phone number)
6. ✅ **Creates session ID** automatically
7. ✅ **Configures and starts** your bot with PM2

**You only need to provide:**
- 📱 Your phone number (with country code)
- � Enter the 8-digit code in WhatsApp
- ⚙️ Optional: Bot prefix and admin numbers

**No manual cloning, no session generator websites, no complex setup!**

---

## 🎯 What This Command Does

1. ✅ **Downloads YOUR deployment script** from GitHub
2. ✅ **Installs all dependencies** (Node.js 20, Yarn, PM2, Git, FFmpeg)
3. ✅ **Clones YOUR repository** (`https://github.com/Investor45/kentech-multibot.git`)
4. ✅ **Configures environment** (Session ID, prefix, admin settings)
5. ✅ **Starts bot with PM2** (auto-restart enabled)
6. ✅ **Sets up firewall** (basic security)
7. ✅ **Creates systemd service** (optional)

---

## 📋 VPS Requirements

- **OS**: Ubuntu 20.04+ or Debian 10+
- **RAM**: 512MB minimum (1GB recommended)
- **Storage**: 1GB free space
- **Access**: Root or sudo privileges
- **Network**: Internet connection

---

## 🔧 Deployment Process

### Step 1: SSH to Your VPS
```bash
ssh root@your-vps-ip
# or
ssh username@your-vps-ip
```

### Step 2: Run the One-Command Deployment
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

### Step 3: Follow the Automated Setup
The script will automatically:
1. **Install all dependencies** (Node.js, Yarn, PM2, etc.)
2. **Download KENTECH MULTIBOT** from GitHub
3. **Ask for your phone number** (e.g., 237670217260)

### Step 4: Enter Pairing Code in WhatsApp
1. Script generates **8-digit pairing code** (e.g., 12345678)
2. Open **WhatsApp** on your phone
3. Go to **Settings** → **Linked Devices**
4. Tap **"Link a Device"**
5. Tap **"Link with phone number instead"** 
6. **Enter the 8-digit code**

### Step 5: Bot Auto-Configuration
The script automatically:
- ✅ Creates your session ID
- ✅ Configures the bot
- ✅ Starts with PM2
- ✅ Sets up firewall

**Total setup time: 5-10 minutes!**

---

## 🛡️ Security Features

- Firewall configuration (UFW)
- Non-root execution recommendations
- Automatic dependency management
- PM2 process isolation

---

## 📊 Post-Deployment Management

### Check Bot Status
```bash
pm2 status
```

### View Real-time Logs
```bash
pm2 logs kentech-multibot --lines 50
```

### Restart Bot
```bash
pm2 restart kentech-multibot
```

### Update Bot
```bash
cd /home/username/kentech-multibot
git pull
yarn install
pm2 restart kentech-multibot
```

### Stop Bot
```bash
pm2 stop kentech-multibot
```

---

## 🔍 Testing Your Deployment

1. **Check PM2 status**: `pm2 status` (should show "online")
2. **View logs**: `pm2 logs kentech-multibot`
3. **Test bot**: Send `.ping` to your bot on WhatsApp
4. **Check menu**: Send `.menu` to see KENTECH MULTIBOT branding

---

## 🆘 Troubleshooting

### Bot Not Starting
```bash
# Check logs for errors
pm2 logs kentech-multibot

# Check configuration
cat /home/username/kentech-multibot/config.env

# Restart bot
pm2 restart kentech-multibot
```

### Session ID Issues
1. Generate new session ID from your session generator
2. Update config.env: `nano /home/username/kentech-multibot/config.env`
3. Restart bot: `pm2 restart kentech-multibot`

### Dependency Issues
```bash
# Reinstall dependencies
cd /home/username/kentech-multibot
yarn install --force
pm2 restart kentech-multibot
```

---

## 🚀 Advanced Features

### Auto-restart on Boot
```bash
pm2 startup
pm2 save
```

### Monitor Resources
```bash
pm2 monit
```

### Multiple Instances
```bash
# Clone for second instance
git clone https://github.com/Investor45/kentech-multibot.git kentech-multibot-2
# Configure different session ID
# Start with different name
pm2 start index.js --name kentech-multibot-2
```

---

## 📱 Session Generator

Don't forget to deploy your session generator for users:

1. **Netlify**: Drag & drop `kentech-session-static.html`
2. **Vercel**: Import from GitHub
3. **Your VPS**: Serve the session generator files

---

## ✅ Success Indicators

When deployment is successful, you'll see:
- ✅ PM2 shows bot as "online"
- ✅ Bot responds to `.ping` command
- ✅ Menu shows "KENTECH MULTIBOT" branding
- ✅ No "levanter" references anywhere

---

## 🎉 Community Ready

Your KENTECH MULTIBOT is now:
- ✅ Fully branded
- ✅ Deployed on VPS
- ✅ Ready for users
- ✅ Easy to maintain

**Repository**: https://github.com/Investor45/kentech-multibot

---

**Enjoy your KENTECH MULTIBOT deployment! 🚀**
