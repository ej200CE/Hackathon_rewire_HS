# Dietary Recommendations System

An AI-powered system that provides personalized dietary recommendations based on real-time supermarket product data and user preferences.

## 🏗️ Architecture Overview

The system consists of five main modules:

1. **Frontend Module**: User interface for interaction and visualization
2. **Scraping Module**: Automated scraping of supermarket websites with S3 storage
3. **Data Processing Module**: ETL pipeline from S3 to relational database
4. **AI Agents Module**: Intelligent agents for recommendations and nutrition planning
5. **Backend API**: RESTful API connecting all components

## 📁 Project Structure

```
dietary-recommendations/
├── frontend/                 # Frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Application pages
│   │   ├── services/       # API service layer
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── tests/              # Frontend tests
├── scraping/               # Web scraping module
│   ├── scrapers/          # Supermarket-specific scrapers
│   ├── config/            # Scraping configurations
│   ├── utils/             # Scraping utilities
│   └── tests/             # Scraping tests
├── data_processing/        # Data processing module
│   ├── extractors/        # Data extraction from S3
│   ├── transformers/      # Data transformation logic
│   ├── loaders/          # Database loading utilities
│   ├── utils/            # Processing utilities
│   └── tests/            # Processing tests
├── ai_agents/             # AI agents module
│   ├── agents/           # AI agent implementations
│   ├── prompts/          # Prompt templates
│   ├── utils/            # AI utilities
│   └── tests/            # AI agent tests
├── backend/               # Backend API
│   ├── api/              # API endpoints
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── database/         # Database configuration
│   ├── utils/            # Backend utilities
│   └── tests/            # Backend tests
├── config/                # Configuration files
├── scripts/               # Utility scripts
├── docs/                  # Documentation
│   ├── diagrams/         # Architecture diagrams
│   ├── api_reference/    # API documentation
│   └── guides/           # User guides
├── pyproject.toml         # Python project configuration
└── env.example            # Environment variables example
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- AWS Account (for S3)
- Node.js 18+ (for frontend)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dietary-recommendations
```

2. Install uv (Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

4. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
cd scripts
python init_database.py
```

6. Install frontend dependencies:
```bash
cd frontend
npm install
```

## 🛠️ Development

### Running the Backend

```bash
cd backend
uvicorn api.main:app --reload
```

### Running the Frontend

```bash
cd frontend
npm run dev
```

### Running Scrapers

```bash
cd scraping
python -m scrapers.run_scraper --store tesco
```

### Running Data Processing

```bash
cd data_processing
python -m extractors.run_etl
```

## 📊 Database Schema

See `docs/diagrams/database_schema.md` for detailed database structure.

## 🤖 AI Agents

The system includes multiple AI agents:

- **Recommendation Agent**: Provides personalized product recommendations
- **Nutrition Planner**: Creates and refines nutrition plans
- **Shopping Assistant**: Helps optimize shopping lists

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run specific module tests:
```bash
pytest scraping/tests/
pytest backend/tests/
```

## 📚 Documentation

- [API Reference](docs/api_reference/README.md)
- [Scraping Guide](docs/guides/scraping.md)
- [AI Agent Configuration](docs/guides/ai_agents.md)
- [Deployment Guide](docs/guides/deployment.md)

## 🤝 Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
