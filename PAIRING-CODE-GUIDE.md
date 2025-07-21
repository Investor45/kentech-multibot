# 📱 KENTECH MULTIBOT - Pairing Code Guide

## 🚀 How to Get Your Session ID Using Pairing Code

### Method 1: Using Pairing Code (Recommended)

**Step 1: Run the Pairing Code Generator**
```bash
cd your-kentech-multibot-folder
npm run pairing
```

**Step 2: Enter Your Phone Number**
- Enter your WhatsApp phone number with country code
- Example: `237670217260` (no + sign needed)

**Step 3: Get Your Pairing Code**
- The script will generate a 8-digit pairing code
- Example: `12345678`

**Step 4: Enter Code in WhatsApp**
1. Open WhatsApp on your phone
2. Go to **Settings** > **Linked Devices** 
3. Tap **"Link a Device"**
4. Tap **"Link with phone number instead"** 
5. Enter the 8-digit code when prompted

**Step 5: Copy Your Session ID**
- Once connected, your session ID will be displayed
- Copy the entire session ID (starts with `kentech_multibot_`)
- It will also be saved to `session_id.txt` file

### Method 2: Using QR Code (Alternative)

```bash
npm run qr
```
- Scan the QR code with WhatsApp Web scanner
- Your session ID will be generated

## 🔧 Using Your Session ID

1. **Open `config.env` file**
2. **Find this line:**
   ```
   SESSION_ID=kentech_multibot_sessionid
   ```
3. **Replace with your actual session ID:**
   ```
   SESSION_ID=kentech_multibot_eyJub2lzZUtleSI6eyJwcml2YXRlIjp7InR5cGUiOiJCdWZmZXIiLCJkYXRhIjoiYUk4...
   ```
4. **Save the file**

## 🚀 Deploy Your Bot

After setting your session ID, deploy using:

**VPS Deployment:**
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Investor45/kentech-multibot/master/deploy.sh)
```

**Local Testing:**
```bash
npm run dev
```

## ⚠️ Important Notes

- **Keep your session ID secure** - never share it publicly
- **One session ID per phone number** - each number needs its own session
- **Session expires** if not used for 7+ days
- **Re-generate if needed** using the same process

## 🔧 Troubleshooting

**"Invalid phone number" error:**
- Make sure to include country code (e.g., 237670217260)
- Don't include + or spaces
- Use only numbers

**"Pairing code expired" error:**
- Run the script again to get a new code
- Enter the code quickly (codes expire in 60 seconds)

**"Connection failed" error:**
- Check your internet connection
- Make sure WhatsApp is working on your phone
- Try running the script again

## 📞 Example Phone Number Formats

| Country | Example | Format |
|---------|---------|---------|
| Cameroon | +237 670 21 72 60 | 237670217260 |
| Nigeria | +234 803 123 4567 | 2348031234567 |
| USA | +1 (555) 123-4567 | 15551234567 |
| India | +91 98765 43210 | 919876543210 |

**Remember:** No + sign, no spaces, just numbers with country code!
