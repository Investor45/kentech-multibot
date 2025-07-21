# Contributing to KENTECH MULTIBOT

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to KENTECH MULTIBOT. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the JavaScript/Node.js styleguides
- Include thoughtfully-worded, well-structured tests
- Document new code based on the Documentation Styleguide
- End all files with a newline

## Development Environment Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/kentech-multibot.git`
3. Navigate to the directory: `cd kentech-multibot`
4. Install dependencies: `yarn install`
5. Copy config: `cp config.env.example config.env`
6. Configure your environment variables
7. Start development: `yarn dev`

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### JavaScript Styleguide

- Use 2 spaces for indentation
- Prefer const over let, let over var
- Use semicolons
- Use single quotes for strings
- Use template literals for string interpolation
- Use arrow functions when appropriate

### Documentation Styleguide

- Use Markdown
- Reference functions and classes in backticks
- Include code examples where helpful

## Project Structure

```
kentech-multibot/
├── lib/                 # Core library files
│   ├── client.js       # Main bot client
│   ├── events.js       # Event handlers
│   └── utils.js        # Utility functions
├── plugins/             # Bot commands/plugins
├── lang/               # Language files
├── media/              # Media assets
├── config.env          # Environment configuration
└── index.js           # Entry point
```

## Adding New Commands

To add a new command:

1. Create a new file in the `plugins/` directory
2. Follow the existing command structure:

```javascript
const { command } = require('../lib/events')

command(
  {
    pattern: 'yourcommand',
    fromMe: false,
    desc: 'Description of your command'
  },
  async (message, match) => {
    // Your command logic here
    await message.reply('Hello from your command!')
  }
)
```

3. Test your command thoroughly
4. Add documentation to the README if necessary

## Adding Language Support

To add a new language:

1. Create a new JSON file in the `lang/` directory (e.g., `lang/your_language.json`)
2. Follow the structure of existing language files
3. Add the language code to the supported languages list in README.md
4. Test all translations

## Questions?

Don't hesitate to ask questions by creating an issue with the question label or joining our community channels mentioned in the README.

Thank you for contributing! 🚀
