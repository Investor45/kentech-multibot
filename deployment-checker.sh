#!/bin/bash

# 🔍 KENTECH MULTIBOT Deployment Checker
# Run this script to verify your deployment is working

echo "🔍 KENTECH MULTIBOT Deployment Checker"
echo "======================================"

# Function to check URL
check_url() {
    local url=$1
    local name=$2
    echo -n "🌐 Checking $name... "
    
    if curl -s --head "$url" | head -n 1 | grep -q "200 OK"; then
        echo "✅ ONLINE"
    else
        echo "❌ OFFLINE"
    fi
}

# Check if session generator is deployed
echo ""
echo "📱 SESSION GENERATOR CHECKS:"
echo "----------------------------"

read -p "Enter your session generator URL (e.g., https://yoursite.netlify.app): " session_url

if [ ! -z "$session_url" ]; then
    check_url "$session_url" "Session Generator"
    echo "📱 Test: Open $session_url in browser and try generating QR"
else
    echo "⚠️  No session generator URL provided"
fi

# Check if main bot is deployed
echo ""
echo "🤖 MAIN BOT CHECKS:"
echo "------------------"

read -p "Enter your bot deployment URL (e.g., https://yourbot.railway.app): " bot_url

if [ ! -z "$bot_url" ]; then
    check_url "$bot_url" "Main Bot"
    echo "🤖 Test: Send '.ping' command to your bot"
else
    echo "⚠️  No bot URL provided"
fi

# Check GitHub repository
echo ""
echo "📂 GITHUB REPOSITORY:"
echo "--------------------"

read -p "Enter your GitHub username: " github_user

if [ ! -z "$github_user" ]; then
    repo_url="https://github.com/$github_user/kentech-multibot"
    check_url "$repo_url" "GitHub Repository"
    echo "📂 Repository: $repo_url"
else
    echo "⚠️  No GitHub username provided"
fi

# Local environment check
echo ""
echo "💻 LOCAL ENVIRONMENT:"
echo "--------------------"

# Check Node.js
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✅ Node.js: $node_version"
else
    echo "❌ Node.js not installed"
fi

# Check Git
if command -v git &> /dev/null; then
    git_version=$(git --version)
    echo "✅ $git_version"
else
    echo "❌ Git not installed"
fi

# Check package.json
if [ -f "package.json" ]; then
    echo "✅ package.json found"
    
    # Check if it's KENTECH branded
    if grep -q "kentech-multibot" package.json; then
        echo "✅ KENTECH branding confirmed"
    else
        echo "⚠️  Still has old branding"
    fi
else
    echo "❌ package.json not found"
fi

# Check config.env
if [ -f "config.env" ]; then
    echo "✅ config.env found"
    
    # Check session ID
    if grep -q "YOUR_ACTUAL_SESSION_ID_HERE" config.env; then
        echo "⚠️  Session ID still placeholder - update with real session ID"
    else
        echo "✅ Session ID appears to be configured"
    fi
else
    echo "❌ config.env not found"
fi

echo ""
echo "🎯 DEPLOYMENT STATUS SUMMARY:"
echo "=============================="

echo "📋 TODO CHECKLIST:"
echo "[ ] Session generator deployed and working"
echo "[ ] GitHub repository created and public"
echo "[ ] Main bot deployed to cloud platform"
echo "[ ] Session ID generated and configured"
echo "[ ] Bot tested with .ping command"
echo "[ ] Documentation updated with your URLs"

echo ""
echo "🆘 NEED HELP?"
echo "- Check DEPLOYMENT.md for detailed instructions"
echo "- Check BOT-DEPLOYMENT.md for bot-specific deployment"
echo "- Check VERCEL-DEPLOY.md for session generator deployment"
echo "- Check GIT-COMMANDS.md for repository setup"

echo ""
echo "✅ Deployment checker complete!"
