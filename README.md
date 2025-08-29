# HSBC AI-Powered Wealth Operation

## Overview

To solve HSBC's inefficient operations and process, this application is a solution that leverages AI to solve that problem.

Assuming that the AI model is already pre-trained with HSBC's products, policies etc.

This application takes in data such as client demographics, annual income, assets, passes it into the AI for processing, and creates a summary of the client and the product recommended for them.


## Configuration

### Create environment file

```bash
cp dotenv.template .env
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python -m app.run
```