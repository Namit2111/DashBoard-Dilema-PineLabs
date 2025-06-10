# Natural Language to SQL Query Assistant

This project is an intelligent assistant that converts natural language questions into SQL queries and provides insightful answers about your data. It uses FastAPI for the backend, Google's Generative AI for natural language processing, and provides both a web interface and API endpoints for interaction.

## 🌟 Features

- Natural language to SQL query conversion
- Interactive web interface
- RESTful API endpoints
- Rate limiting for API calls
- Database schema introspection
- Intelligent query generation with context awareness
- Support for complex business queries
- Automatic result summarization for large datasets

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Template Engine**: Jinja2
- **Database**: SQLite
- **AI/ML**: Google Generative AI
- **Data Processing**: Pandas
- **Development Server**: Uvicorn

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd PineLabs
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8000`

## 🔄 API Endpoints

- `GET /`: Web interface for query input
- `POST /`: Process natural language query
- `GET /monitor`: Check API usage statistics
- `HEAD /ping`: Health check endpoint
- `GET /tables`: Get database schema and sample data

## 🏗️ Project Structure

```
PineLabs/
├── agent/              # AI agent implementation
├── config/             # Configuration files
├── data/               # Data files
├── templates/          # HTML templates
├── utils/              # Utility functions
├── app.py             # Main FastAPI application
├── pipeline.py        # NL to SQL pipeline implementation
├── bot.py             # Bot implementation
├── requirements.txt   # Python dependencies
└── vercel.json        # Vercel deployment configuration
```

## 🔒 Rate Limiting

The API implements rate limiting with the following constraints:
- Maximum 10 agent calls per minute
- Automatic reset after one minute

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

If you encounter any issues:

1. Check if all dependencies are installed correctly
2. Verify your Google API key is set correctly
3. Ensure your database is properly configured
4. Check the application logs for detailed error messages

## 📞 Support

For support or questions, please open an issue in the repository. 