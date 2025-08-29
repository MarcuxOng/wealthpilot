# Project Setup

## Frontend

```bash
npm install
cd frontend
npm run dev
```

## Backend

```bash
pip install -r requirements.txt
.venv\Scripts\activate
python -m backend.app
```


## Overview

To solve HSBC's inefficient operations and process, this application is a solution that leverages AI to solve that problem.

Assuming that the AI model is already pre-trained with HSBC's products, policies etc.

This application takes in data such as client demographics, annual income, assets, passes it into the AI for processing, and creates a summary of the client and the product recommended for them.