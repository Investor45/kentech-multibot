# Kentech Bot Pairing Application

## Quick Start Guide

### 1. Installation

First, ensure you have Python 3.8+ installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure as needed:

```bash
copy .env.example .env
```

Edit the `.env` file to match your environment.

### 3. Running the Application

#### Option A: Using the startup script (Windows)
```bash
start.bat
```

#### Option B: Direct Python execution
```bash
python main.py
```

#### Option C: Using VS Code
- Press `F5` to run in debug mode
- Or use `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Kentech Bot Pairing App"

### 4. API Access

Once running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Status**: http://localhost:8000/api/status

### 5. Example Usage

Run the API demonstration:
```bash
python examples/api_demo.py
```

Run example bots:
```bash
python examples/example_bot.py "TestBot1" "chatbot"
python examples/example_bot.py "TestBot2" "taskbot"
```

### 6. Development

#### Running Tests
```bash
pytest tests/ -v
```

#### Code Formatting
```bash
black src/ tests/ examples/
isort src/ tests/ examples/
```

#### Type Checking
```bash
mypy src/
```

## API Endpoints

### Bots
- `POST /api/bots` - Register a new bot
- `GET /api/bots` - List all bots
- `GET /api/bots/{bot_id}` - Get specific bot
- `PUT /api/bots/{bot_id}` - Update bot
- `POST /api/bots/{bot_id}/heartbeat` - Update heartbeat
- `DELETE /api/bots/{bot_id}` - Deregister bot

### Bot Pairs
- `POST /api/pairs` - Create bot pair
- `GET /api/pairs` - List all pairs
- `GET /api/pairs/active` - List active pairs
- `GET /api/pairs/{pair_id}` - Get specific pair
- `DELETE /api/pairs/{pair_id}` - Terminate pair
- `POST /api/pairs/auto` - Auto-pair bots

### System
- `GET /api/status` - System status
- `GET /api/strategies` - Available strategies
- `GET /health` - Health check

## WebSocket Endpoints

### Bot Connection
- `ws://localhost:8000/ws/bot/{bot_id}` - Bot WebSocket connection

### Monitoring
- `ws://localhost:8000/ws/monitor` - Real-time monitoring

## Pairing Strategies

1. **Default**: Random pairing of available bots
2. **Capability-based**: Pairs bots with complementary capabilities
3. **Type-based**: Pairs bots of different types when possible

## Project Structure

```
kentech-pairing-app/
├── src/                     # Source code
│   ├── api/                # API routes and WebSocket handlers
│   ├── bots/               # Bot management
│   ├── config/             # Configuration and database
│   ├── monitoring/         # Health checks and metrics
│   ├── pairing/            # Pairing logic and algorithms
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── examples/               # Example scripts
├── .vscode/                # VS Code configuration
├── logs/                   # Application logs
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the PORT in .env file
2. **Database errors**: Delete the database file and restart
3. **Import errors**: Ensure all dependencies are installed
4. **WebSocket connection issues**: Check firewall settings

### Logs

Application logs are stored in the `logs/` directory:
- `app.log` - General application logs
- `errors.log` - Error-specific logs

## Contributing

1. Follow PEP 8 style guidelines
2. Add tests for new functionality
3. Update documentation as needed
4. Use type hints throughout

## License

Copyright © 2025 Kentech Systems
