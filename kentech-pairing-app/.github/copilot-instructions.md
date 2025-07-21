<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Kentech Bot Pairing Application - Copilot Instructions

This is a Python-based bot pairing application for managing multiple bots in the Kentech ecosystem.

## Project Context
- **Purpose**: Intelligent bot pairing and management system
- **Architecture**: Async Python with FastAPI, WebSockets, and Redis
- **Database**: SQLAlchemy with async support
- **Monitoring**: Real-time metrics and health checks

## Code Style Guidelines
- Follow PEP 8 for Python code style
- Use async/await for all I/O operations
- Use type hints throughout the codebase
- Use Pydantic models for data validation
- Use loguru for structured logging

## Key Components
1. **Pairing Logic**: Located in `src/pairing/` - handles bot matching algorithms
2. **Bot Management**: Located in `src/bots/` - manages bot lifecycle and registry
3. **API Layer**: Located in `src/api/` - REST and WebSocket endpoints
4. **Configuration**: Located in `src/config/` - centralized settings management
5. **Monitoring**: Located in `src/monitoring/` - metrics and health monitoring

## Dependencies
- FastAPI for web framework
- Pydantic for data validation
- SQLAlchemy for database ORM
- Redis for caching and pub/sub
- WebSockets for real-time communication
- Loguru for logging

## Testing
- Use pytest for all tests
- Write async tests with pytest-asyncio
- Mock external dependencies
- Aim for high test coverage

## Best Practices
- Always handle exceptions gracefully
- Use dependency injection for testability
- Implement proper error responses for API endpoints
- Use environment variables for configuration
- Log important events and errors
- Validate all input data with Pydantic
