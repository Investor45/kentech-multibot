#!/bin/bash

# KENTECH MULTIBOT - VPS Deployment Script
# This script automates the deployment of KENTECH MULTIBOT on Ubuntu/Debian VPS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
    echo -e "${GREEN}[KENTECH MULTIBOT]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# ASCII Art Banner
print_banner() {
    echo -e "${GREEN}"
    echo "╦╔═╔═╗╔╗╔╔╦╗╔═╗╔═╗╦ ╦  ╔╦╗╦ ╦╦ ╔╦╗╦╔╗ ╔═╗╔╦╗"
    echo "╠╩╗║╣ ║║║ ║ ║╣ ║  ╠═╣  ║║║║ ║║  ║ ║╠╩╗║ ║ ║ "
    echo "╩ ╩╚═╝╝╚╝ ╩ ╚═╝╚═╝╩ ╩  ╩ ╩╚═╝╩═╝╩ ╩╚═╝╚═╝ ╩ "
    echo "                                                "
    echo "         WhatsApp Bot Deployment Script         "
    echo -e "${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "This script should not be run as root for security reasons."
        read -p "Do you want to continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Deployment cancelled."
            exit 1
        fi
    fi
}

# Update system packages
update_system() {
    print_message "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    print_message "System updated successfully!"
}

# Install Node.js
install_nodejs() {
    print_message "Installing Node.js 20.x..."
    
    # Remove old Node.js versions if they exist
    if command -v node &> /dev/null; then
        print_info "Removing existing Node.js installation..."
        sudo apt remove nodejs npm -y
    fi
    
    # Install Node.js 20.x
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install nodejs -y
    
    # Verify installation
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    print_message "Node.js installed: $NODE_VERSION"
    print_message "npm installed: $NPM_VERSION"
}

# Install system dependencies
install_dependencies() {
    print_message "Installing system dependencies..."
    sudo apt install git ffmpeg wget curl build-essential python3 make g++ -y
    print_message "System dependencies installed!"
}

# Install Yarn
install_yarn() {
    print_message "Installing Yarn package manager..."
    sudo npm install -g yarn
    YARN_VERSION=$(yarn --version)
    print_message "Yarn installed: v$YARN_VERSION"
}

# Install PM2
install_pm2() {
    print_message "Installing PM2 process manager..."
    sudo npm install -g pm2
    PM2_VERSION=$(pm2 --version)
    print_message "PM2 installed: v$PM2_VERSION"
}

# Clone repository
clone_repository() {
    print_message "Cloning KENTECH MULTIBOT repository..."
    
    # Default repository URL
    REPO_URL="https://github.com/Investor45/kentech-multibot.git"
    
    # Default installation directory
    INSTALL_DIR="/home/$USER/kentech-multibot"
    
    print_info "Repository: $REPO_URL"
    print_info "Installation directory: $INSTALL_DIR"
    
    # Remove existing directory if it exists
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Directory $INSTALL_DIR already exists. Removing..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Clone repository
    print_message "Downloading KENTECH MULTIBOT..."
    git clone "$REPO_URL" "$INSTALL_DIR" || {
        print_error "Failed to clone repository. Please check your internet connection."
        exit 1
    }
    
    cd "$INSTALL_DIR"
    print_message "✅ Repository cloned successfully!"
}

# Install bot dependencies
install_bot_dependencies() {
    print_message "Installing bot dependencies..."
    
    # Configure git to use HTTPS instead of SSH for all Git repositories
    git config --global url."https://github.com/".insteadOf git@github.com:
    git config --global url."https://github.com/".insteadOf ssh://git@github.com/
    git config --global url."https://".insteadOf git://
    
    # Remove existing lock files to avoid conflicts
    rm -f package-lock.json yarn.lock
    
    # Install dependencies with npm instead of yarn to avoid SSH issues
    print_info "Installing with npm to avoid SSH dependency issues..."
    npm install --legacy-peer-deps
    
    # Rebuild sqlite3 to fix native binding issues
    print_info "Rebuilding sqlite3 for Node.js compatibility..."
    npm rebuild sqlite3 || {
        print_warning "sqlite3 rebuild failed, trying alternative installation..."
        npm uninstall sqlite3
        npm install sqlite3@5.1.6 --legacy-peer-deps
    }
    
    print_message "Bot dependencies installed!"
}

# Get session ID from user
get_session_id() {
    print_message "🔑 WhatsApp Session ID Configuration"
    echo
    print_info "To connect your bot to WhatsApp, you need a session ID."
    print_info "Generate it using: https://levanter-delta.vercel.app/"
    echo
    print_info "Instructions:"
    print_info "1. Visit: https://levanter-delta.vercel.app/"
    print_info "2. Enter your phone number"
    print_info "3. Follow the pairing instructions"
    print_info "4. Copy the generated session ID"
    echo
    
    while [ -z "$SESSION_ID" ]; do
        read -p "� Paste your session ID here: " SESSION_ID
        if [ -z "$SESSION_ID" ]; then
            print_error "Session ID is required!"
        elif [ ${#SESSION_ID} -lt 20 ]; then
            print_error "Session ID seems too short. Please check and try again."
            SESSION_ID=""
        fi
    done
    
    print_message "✅ Session ID received!"
    return 0
}

# Configure environment
configure_environment() {
    print_message "Configuring bot environment..."
    
    # Create config.env if it doesn't exist
    if [ ! -f "config.env" ]; then
        if [ -f "config.env.example" ]; then
            cp config.env.example config.env
            print_message "Created config.env from example file."
        else
            print_error "No config.env.example found!"
            exit 1
        fi
    fi
    
    print_info "🎯 KENTECH MULTIBOT Configuration"
    echo
    
    # Get bot name
    read -p "Enter your bot name [KENTECH MULTIBOT]: " BOT_NAME
    BOT_NAME=${BOT_NAME:-"KENTECH MULTIBOT"}
    print_message "Bot name: $BOT_NAME"
    
    # Get session ID from user
    if ! get_session_id; then
        print_error "Session configuration failed. Deployment cannot continue."
        exit 1
    fi
    
    # Configure session ID
    sed -i "s/SESSION_ID=.*/SESSION_ID=$SESSION_ID/" config.env
    print_message "✅ Session ID configured!"
    
    # Get bot prefix
    read -p "Enter bot prefix [.]: " PREFIX
    PREFIX=${PREFIX:-.}
    sed -i "s/PREFIX=.*/PREFIX=$PREFIX/" config.env
    
    # Get admin phone numbers
    print_info "Configure admin users (optional):"
    read -p "Enter admin phone numbers (comma-separated, with country code) [skip]: " SUDO
    if [ ! -z "$SUDO" ]; then
        sed -i "s/SUDO=.*/SUDO=$SUDO/" config.env
        print_message "Admin users configured: $SUDO"
    fi
    
    # Get bot language
    echo
    print_info "Available languages: en, es, hi, fr, ar, ru, bn, tr, id, ur"
    read -p "Enter bot language [en]: " BOT_LANG
    BOT_LANG=${BOT_LANG:-en}
    sed -i "s/BOT_LANG=.*/BOT_LANG=$BOT_LANG/" config.env
    
    print_message "✅ Environment configured successfully!"
}

# Setup PM2
setup_pm2() {
    print_message "Setting up PM2..."
    
    # Stop any existing PM2 processes
    pm2 stop kentech-multibot 2>/dev/null || true
    pm2 delete kentech-multibot 2>/dev/null || true
    
    # Start the bot with PM2
    pm2 start index.js --name kentech-multibot
    
    # Save PM2 configuration
    pm2 save
    
    # Setup PM2 startup script
    PM2_STARTUP_CMD=$(pm2 startup | tail -n 1)
    if [[ $PM2_STARTUP_CMD == sudo* ]]; then
        print_info "Setting up PM2 auto-startup..."
        eval "$PM2_STARTUP_CMD"
    fi
    
    print_message "PM2 setup completed!"
}

# Setup firewall
setup_firewall() {
    print_message "Configuring firewall..."
    
    # Install ufw if not installed
    if ! command -v ufw &> /dev/null; then
        sudo apt install ufw -y
    fi
    
    # Configure firewall rules
    sudo ufw --force reset
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    
    print_message "Firewall configured!"
}

# Create systemd service (alternative to PM2)
create_systemd_service() {
    read -p "Do you want to create a systemd service instead of using PM2? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "Creating systemd service..."
        
        sudo tee /etc/systemd/system/kentech-multibot.service > /dev/null <<EOF
[Unit]
Description=KENTECH MULTIBOT
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$(which node) index.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
        
        sudo systemctl daemon-reload
        sudo systemctl enable kentech-multibot
        sudo systemctl start kentech-multibot
        
        print_message "Systemd service created and started!"
    fi
}

# Display final information
display_final_info() {
    echo
    print_message "🎉 KENTECH MULTIBOT deployed successfully!"
    echo
    print_info "Bot Name: $BOT_NAME"
    print_info "Bot installed in: $INSTALL_DIR"
    print_info "Configuration file: $INSTALL_DIR/config.env"
    echo
    print_info "Useful commands:"
    echo "  • Check bot status: pm2 status"
    echo "  • View bot logs: pm2 logs kentech-multibot"
    echo "  • Restart bot: pm2 restart kentech-multibot"
    echo "  • Stop bot: pm2 stop kentech-multibot"
    echo "  • Update bot: git pull && npm install && pm2 restart kentech-multibot"
    echo
    
    print_message "Session ID configured: ✅"
    print_info "Your $BOT_NAME is ready and running!"
    echo
    print_info "Testing bot startup..."
    sleep 2
    pm2 logs kentech-multibot --lines 10
    
    echo
    print_message "Join our community:"
    print_info "• GitHub: https://github.com/Investor45/kentech-multibot"
    print_info "• Support: Create an issue on GitHub"
    echo
}

# Main deployment function
main() {
    print_banner
    
    print_info "Starting KENTECH MULTIBOT deployment..."
    print_warning "This script will install Node.js, dependencies, and configure the bot."
    echo
    
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Deployment cancelled."
        exit 1
    fi
    
    check_root
    update_system
    install_nodejs
    install_dependencies
    install_yarn
    install_pm2
    clone_repository
    install_bot_dependencies
    configure_environment
    setup_firewall
    setup_pm2
    create_systemd_service
    display_final_info
}

# Error handling
trap 'print_error "Deployment failed! Check the error above."; exit 1' ERR

# Run main function
main "$@"