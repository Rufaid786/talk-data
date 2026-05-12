
# TalkData: Your Data Companion

TalkData is an intelligent data analysis platform built with Streamlit and powered by a multi-agent system using LangGraph. It allows users to interact with their data through natural language queries, supporting both uploaded datasets (CSV/Excel) and direct connections to Snowflake databases.

## Features

- **Natural Language Data Interaction**: Ask questions about your data in plain English
- **Multi-Agent Architecture**: Intelligent routing between different data sources and analysis types
- **File Upload Support**: Users can upload Excel or csv files and ask their queries
- **Snowflake Integration**: Direct querying of Snowflake Warehouse
- **Real-time Chat Interface**: Conversational AI experience

## Installation

### Prerequisites

- Python 3.8 or higher
- Access to Snowflake account 
- Google API key for Gemini model

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd talk-data
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here

   # Optional: Snowflake configuration (The credentails of the snowflake warehouse which you need to connect with)
   SNOWFLAKE_USER=your_snowflake_username
   SNOWFLAKE_PASSWORD=your_snowflake_password
   SNOWFLAKE_ACCOUNT=your_snowflake_account
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   ```

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run main.py
```

## Architecture

TalkData uses a multi-agent system built with LangGraph:

- **Supervisor Agent**: Routes queries to appropriate specialized agents
- **Snowflake Agent**: Handles database queries and schema exploration
- **Sheet Analysis Agent**: Processes uploaded spreadsheets and CSV files

The system intelligently determines whether to use uploaded data or database connections based on the user's query and available data.

## Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Required for LLM functionality
- `SNOWFLAKE`: Optional, for database connectivity

### Model Configuration

Currently uses Google Gemini 2.5 Flash Lite model. Temperature set to 0 for consistent responses.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'description of your change'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request


## Support

For issues or questions:
- Check the existing issues on GitHub
- Create a new issue with detailed information
- Include error messages, your environment, and steps to reproduce

## Future Enhancements

- Support for additional agents like pdf ,image cpabailities
- Advanced data visualization capabilities
- Multi-language support
- Integration with additional AI models

## Explore
[talk-data.streamlit.app](https://talk-data.streamlit.app/)
