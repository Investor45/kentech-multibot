#!/bin/bash

# 🚀 KENTECH MULTIBOT Quick Deployment Script
# This script helps deploy your bot quickly

echo "🚀 KENTECH MULTIBOT Deployment Helper"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from your KENTECH MULTIBOT directory."
    exit 1
fi

echo "✅ Found KENTECH MULTIBOT project"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists git; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check for session ID
if grep -q "YOUR_ACTUAL_SESSION_ID_HERE" config.env; then
    echo "⚠️  Warning: You still have placeholder session ID"
    echo "📝 Please update your SESSION_ID in config.env first"
    echo "🌐 Use the session generator: https://your-session-generator.vercel.app"
    read -p "Do you want to continue anyway? (y/n): " continue_deploy
    if [ "$continue_deploy" != "y" ]; then
        echo "❌ Deployment cancelled. Please update your session ID first."
        exit 1
    fi
fi

# Deployment options
echo ""
echo "🌐 Choose your deployment platform:"
echo "1) GitHub + Vercel (Recommended)"
echo "2) GitHub + Heroku"
echo "3) VPS Deployment"
echo "4) Railway"
echo "5) Just setup GitHub repository"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Setting up GitHub + Vercel deployment..."
        echo "📝 Manual steps required:"
        echo "   1. Create GitHub repository: https://github.com/new"
        echo "   2. Upload files to repository"
        echo "   3. Connect Vercel: https://vercel.com"
        echo "   4. Import your repository"
        ;;
    2)
        echo "🚀 Setting up GitHub + Heroku deployment..."
        if ! command_exists heroku; then
            echo "❌ Heroku CLI not found. Installing..."
            echo "📝 Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli"
        else
            echo "✅ Heroku CLI found"
            read -p "Enter your Heroku app name: " app_name
            heroku create $app_name
            echo "🔧 Setting environment variables..."
            heroku config:set SESSION_ID=$(grep SESSION_ID config.env | cut -d'=' -f2)
            heroku config:set PREFIX=$(grep PREFIX config.env | cut -d'=' -f2)
        fi
        ;;
    3)
        echo "🚀 VPS Deployment setup..."
        echo "📝 Make sure your VPS has:"
        echo "   - Ubuntu 20.04+ or CentOS 8+"
        echo "   - Root or sudo access"
        echo "   - Internet connection"
        echo ""
        echo "📋 Run this command on your VPS:"
        echo "bash <(curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/kentech-multibot/main/deploy.sh)"
        ;;
    4)
        echo "🚀 Railway deployment setup..."
        echo "📝 Manual steps required:"
        echo "   1. Go to https://railway.app"
        echo "   2. Connect your GitHub account"
        echo "   3. Import your repository"
        echo "   4. Configure environment variables"
        ;;
    5)
        echo "📂 Setting up GitHub repository only..."
        read -p "Enter your GitHub username: " github_user
        echo ""
        echo "📝 Next steps:"
        echo "   1. Go to: https://github.com/new"
        echo "   2. Repository name: kentech-multibot"
        echo "   3. Make it public"
        echo "   4. Run these commands:"
        echo ""
        echo "   git init"
        echo "   git add ."
        echo "   git commit -m '🚀 Initial commit: KENTECH MULTIBOT'"
        echo "   git branch -M main"
        echo "   git remote add origin https://github.com/$github_user/kentech-multibot.git"
        echo "   git push -u origin main"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment setup complete!"
echo "📚 For detailed instructions, check DEPLOYMENT.md"
echo "🌐 Session Generator: Use your deployed session generator to get valid session ID"
echo "🔧 Support: Check GitHub repository for issues and updates"
