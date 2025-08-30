# HSBC AI-Powered Wealth Management System

## Overview

An AI-driven solution for optimizing HSBC's wealth management operations through:

- Client demographic analysis
- Asset and income processing
- Automated product recommendations
- Client summary generation

## Prerequisites

- Node.js v18+ & npm v9+
- Python 3.10+
- Virtual environment (venv)

## Installation & Setup

### Environment Configuration

```bash
cp backend/dotenv.template backend/.env
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate and install dependencies:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

3. Start development server:
```bash
python -m app.run
```

## Project Structure

```
backend/
├── app/
│   ├── router/
│   │   ├── clients.py        # Client management endpoints
│   │   ├── products.py       # Product catalog API
│   │   └── client_analysis.py # AI analysis routes
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ClientInput.jsx   # Client data form
│   │   └── NavBar.jsx        # Navigation component
│   ├── pages/               # Application views
│   │   ├── ClientTable.jsx   # Client listing
│   │   └── ProductsTable.jsx # Product catalog
```

## API Reference

`GET /clients`
- Returns list of all clients

`GET /products`
- Returns list of all products

`GET /client_analysis/{client_id}`
- Queries the data from JSON
- Passes to the system prompt
- Then passes to the AI for processing
- Returns the AI analysis and recommendation

## Development

1. Start backend server:
```bash
cd backend
venv\Scripts\activate
python -m app.run
```

2. In separate terminal, start frontend:
```bash
cd frontend
npm run dev
```

## Contributing

1. Create a new feature branch from `main`
2. Make changes with descriptive commit messages
3. Ensure tests pass and documentation is updated
4. Open a pull request for team review

## AI Model Integration

The system uses a pre-trained AI model incorporating HSBC's product knowledge and policies. Key components include:

- `backend/app/llm/gemini.py`: Core AI processing and recommendation logic
- `backend/app/llm/sysPrompt.py`: System prompts and response templates

## Data Sources

Sample data files located in `backend/app/data/`:
- `client.json`: Demo client records with financial profiles
- `products.json`: HSBC product catalog with specifications
