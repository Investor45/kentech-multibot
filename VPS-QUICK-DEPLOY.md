# 🚀 KENTECH MULTIBOT - VPS Quick Deploy Guide

## ⚡ One-Command VPS Deployment

**Run this single command on your VPS:**

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

**This replaces any old deployment scripts and uses YOUR branded KENTECH MULTIBOT!**

## ⚠️ IMPORTANT: Session ID Required

**Before deploying, you MUST have a valid session ID:**

1. 🚫 **Don't use placeholders** like `YOUR_ACTUAL_SESSION_ID_HERE`
2. ✅ **Get real session ID** from [KENTECH Session Generator](https://kentech-session-generator.vercel.app)
3. 📱 **Scan QR code** with WhatsApp Web
4. 💾 **Copy the generated session ID**

**Without a valid session ID, your bot will NOT work!**

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

### Step 1: Generate Session ID FIRST
**⚠️ IMPORTANT: Get your session ID before running the deployment!**

1. Visit: **[KENTECH Session Generator](https://kentech-session-generator.vercel.app)**
2. Generate and copy your session ID
3. Keep it ready - the deployment script will ask for it

### Step 2: SSH to Your VPS
```bash
ssh root@your-vps-ip
# or
ssh username@your-vps-ip
```

### Step 3: Run the Deployment Command
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

### Step 4: Follow the Prompts
The script will ask for:
- **Session ID**: ⚠️ **REQUIRED** - Enter your real session ID (not placeholder)
- **Repository URL**: `https://github.com/Investor45/kentech-multibot.git`
- **Installation Directory**: `/home/username/kentech-multibot` (default)
- **Bot Prefix**: `.` (default)
- **Admin Phone Numbers**: Your phone number with country code
- **Bot Language**: `en` (default)

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
