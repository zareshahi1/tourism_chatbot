# Tourism Chatbot with LangChain and Neshan API

A sophisticated tourism assistant chatbot that leverages AI to help users plan their journeys. The application integrates multiple tools including search functionality and geocoding to provide comprehensive travel assistance.

## Features

- **AI-Powered Tourism Assistant**: Engages in natural conversations about travel planning
- **Web Search Integration**: Uses JinaSearch to find and summarize travel information
- **Geocoding Service**: Converts addresses to Google Maps links using the Neshan API
- **Multi-Language Support**: Outputs information in the user's input language
- **File Processing**: Supports various document formats (DOCX, PDF, TXT, MD, HTML)
- **Text Processing**: Advanced text cleaning and processing for Persian content

## Architecture

The application is built using:
- **LangChain**: For AI chain orchestration
- **LangGraph**: For state management in conversation flows
- **OpenAI GPT-4o**: As the main model for conversation
- **OpenAI GPT-5 Nano**: For summarizing search results
- **Neshan API**: For geocoding addresses
- **JinaSearch**: For web search capabilities

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tourism-chatbot
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the project root based on the `.env.sample`:
```bash
cp .env.sample .env
```

## Configuration

Add the following environment variables to your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `JINA_API_KEY`: Your Jina API key for search functionality
- `NESHAN_API_KEY`: Your Neshan API key for geocoding
- `OPENROUTER_API_KEY`: (Optional) Your OpenRouter API key if using alternative models

## Usage

Run the chatbot application:

```bash
python main.py
```

The application will start an interactive CLI session where you can ask questions about travel, get recommendations, find locations, and receive geocoded results.

Example conversation flows:
- "Find places to visit in Tehran"
- "Where is Golestan Palace?" (Will return a Google Maps link)
- "What's the weather like in Isfahan?"

## Project Structure

```
tourism-chatbot/
├── main.py               # Main application logic and chatbot interface
├── map.py                # Geocoding functionality
├── files.py              # File handling utilities
├── requirements.txt      # Project dependencies
├── .env.sample          # Environment variable template
├── .gitignore           # Git ignore configuration
├── utils/               # Utility functions and modules
│   ├── docx2md.py       # DOCX to Markdown conversion
│   ├── input_adapter.py # Input format adapter
│   ├── text_processing.py # Text cleaning and processing
│   └── loaders/         # File format loaders
├── tests/               # Unit tests
└── uploads/             # Upload directory for files
```

## Modules

### main.py
Contains the core chatbot logic with a LangGraph workflow that processes user input, calls tools when needed, and manages conversation state.

### map.py
Provides geocoding functionality to convert text addresses to Google Maps links using the Neshan API.

### utils/
Collection of utility modules:
- **docx2md.py**: Converts DOCX files to HTML and Markdown
- **input_adapter.py**: Handles multiple input formats (PDF, DOCX, TXT, etc.)
- **text_processing.py**: Advanced text processing with Persian language support
- **loaders/**: Format-specific loaders for different file types

### tests/
Comprehensive unit tests for all modules with proper mocking and error handling.

## Development

### Running Tests

To run the test suite:
```bash
python -m pytest tests/ -v
```

### Adding New Features

1. Add your functionality to the appropriate module
2. Write corresponding unit tests in the `tests/` directory
3. Update this README if necessary

## API Keys Management

For security reasons:
- Never commit your `.env` file to version control
- Use strong, unique API keys
- Regularly rotate your API keys
- Set up usage limits where possible in API provider dashboards

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure all required environment variables are set in your `.env` file
2. **Import Errors**: Make sure all dependencies are installed using `pip install -r requirements.txt`
3. **Geocoding Issues**: Verify that your Neshan API key is valid and has geocoding permissions

### Error Messages

- `"No module named 'langchain_core'"`: Install dependencies with `pip install -r requirements.txt`
- `"API Key not found"`: Check that environment variables are properly set
- `"Rate limit exceeded"`: Throttle your requests or upgrade your API plan

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`python -m pytest tests/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [LangChain](https://python.langchain.com/) for the AI orchestration framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) for state management
- [OpenAI](https://platform.openai.com/) for the language models
- [Neshan API](https://neshan.org/) for geocoding services
- [Jina AI](https://jina.ai/) for search capabilities