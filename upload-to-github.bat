@echo off
echo 🚀 KENTECH MULTIBOT Upload Script
echo ================================

echo.
echo ✅ Step 1: Create repository on GitHub
echo    - Go to: https://github.com/new
echo    - Name: kentech-multibot
echo    - Description: KENTECH MULTIBOT - Advanced WhatsApp Bot
echo    - Make it PUBLIC
echo    - Click Create Repository
echo.

pause

echo.
echo ✅ Step 2: Uploading files...
git remote remove origin 2>nul
git remote add origin https://github.com/Investor45/kentech-multibot.git
git push -u origin master

echo.
echo 🎉 Upload complete!
echo Repository: https://github.com/Investor45/kentech-multibot
echo.

pause
