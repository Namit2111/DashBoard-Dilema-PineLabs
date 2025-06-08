# Natural Language to SQL Query Bot

A Slack bot that converts natural language questions into SQL queries and provides insights from your database. The bot uses a pipeline of AI agents to understand the query, identify relevant tables and columns, generate SQL, and provide meaningful insights.

## Project Structure

```
├── main.py           # Core NL to SQL pipeline implementation
├── bot.py            # Slack bot implementation
├── agent/            # AI agents and prompts
├── utils/            # Database and utility functions
├── config/           # Configuration files
└── data/            # Data related files
```


## Setup and Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [project-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the config directory with:
```
SLACK_BOT_TOKEN=your-bot-token
SLACK_APP_TOKEN=your-app-token
DB_CONNECTION_STRING=your-database-connection-string
```

## Running the Project

1. Run as a standalone query tool:
```bash
python main.py
```

2. Run as a Slack bot:
```bash
python bot.py
```

The bot will respond to:
- Direct mentions (@bot-name)
- Messages containing "hi" in channels where the bot is present

## Features

- Natural language to SQL query conversion
- Progress updates during query processing
- Support for complex database queries
- Automatic data summarization for large result sets
- Interactive Slack bot interface 