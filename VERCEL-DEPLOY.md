# Session Generator Deployment - Vercel

## 🚀 Deploy to Vercel (Easiest)

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign in with GitHub**
3. **Create new project**
4. **Upload these files:**
   - `kentech-session-generator.html` (rename to `index.html`)
   - `kentech-session-server.js` (as `api/session.js`)
   - `session-package.json` (as `package.json`)
   - `vercel-session.json` (as `vercel.json`)

## 📂 Folder Structure for Vercel:
```
session-generator/
├── index.html              # Your kentech-session-generator.html
├── package.json            # Your session-package.json
├── vercel.json             # Your vercel-session.json
└── api/
    └── session.js          # Your kentech-session-server.js
```

## 🔧 Quick Setup:
1. Create new folder: `session-generator`
2. Copy files with new names
3. Upload to Vercel
4. Done! Your session generator will be live

## 🌐 Your URL will be:
`https://your-project-name.vercel.app`

---

# Alternative: GitHub + Vercel Auto-Deploy

1. Create GitHub repo: `kentech-session-generator`
2. Upload files
3. Connect Vercel to GitHub
4. Auto-deploy on every push!
