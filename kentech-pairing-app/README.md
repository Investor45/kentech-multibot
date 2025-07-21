# Kentech Bot Pairing Application

A comprehensive bot pairing system for managing and coordinating multiple bots in the Kentech ecosystem.

## Features

- **Bot Registration & Management**: Register and manage multiple bot instances
- **Intelligent Pairing Logic**: Advanced algorithms for optimal bot pairing
- **Real-time Monitoring**: Live monitoring of bot status and performance
- **Configuration Management**: Flexible configuration system
- **API Interface**: RESTful API for external integrations
- **WebSocket Support**: Real-time communication between bots

## Project Structure

```
kentech-pairing-app/
├── src/
│   ├── pairing/
│   │   ├── __init__.py
│   │   ├── core.py              # Core pairing logic
│   │   ├── algorithms.py        # Pairing algorithms
│   │   └── strategies.py        # Different pairing strategies
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── manager.py           # Bot management
│   │   ├── registry.py          # Bot registration
│   │   └── models.py            # Bot data models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py            # API endpoints
│   │   └── websockets.py        # WebSocket handlers
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuration management
│   │   └── database.py          # Database configuration
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── metrics.py           # Performance metrics
│   │   └── health.py            # Health checks
│   └── utils/
│       ├── __init__.py
│       ├── logger.py            # Logging utilities
│       └── helpers.py           # Helper functions
├── tests/
├── config/
├── logs/
├── .env.example
├── requirements.txt
├── main.py
└── README.md
```

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

## Configuration

The application uses environment variables for configuration. See `.env.example` for available options.

## API Endpoints

- `GET /api/bots` - List all registered bots
- `POST /api/bots` - Register a new bot
- `GET /api/pairs` - Get current bot pairs
- `POST /api/pairs` - Create new bot pairs
- `GET /api/health` - Health check endpoint

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines.

## License

Copyright © 2025 Kentech Systems
