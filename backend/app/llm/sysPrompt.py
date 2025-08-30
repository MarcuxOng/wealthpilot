from typing import Dict

def system_prompt(client_data: Dict, available_products: Dict) -> str:
    products_list = "\n".join([
        f"- {prod['id']}: {prod['name']} ({prod['risk_level']} risk) - {prod['description']}"
        for prod in available_products["products"]
    ])


    response_format = {
        "client_summary": {
            "profile_overview": "Brief overview of client's financial situation",
            "key_insights": [
                "Key insight 1 about the client",
                "Key insight 2 about the client",
                "Key insight 3 about the client"
            ],
            "risk_assessment": "Assessment of client's risk tolerance and capacity"
        },
        "recommendations": [
            {
                "product_id": "1",
                "product_name": "HSBC Retirement Fund",
                "reason": "Detailed explanation of why this product suits the client based on their specific data points",
                "risk_level": "low",
                "confidence": 0.85,
                "priority": "high"
            }
        ]
    }

    prompt = f"""
            You are an expert HSBC Wealth Manager AI assistant. Analyze the provided client data and generate both a client summary and personalized product recommendations.
            
            CLIENT DATA:
            - Name: {client_data['name']}
            - Age: {client_data['age']}
            - Annual Income: ${client_data['annual_income']:,}
            - Risk Profile: {client_data['risk_profile']}
            - Investment Goals: {', '.join(client_data['investment_goals'])}
            - Time Horizon: {client_data['time_horizon']}
            - Current Savings: ${client_data['current_savings']:,}
            - Monthly Surplus: ${client_data['monthly_surplus']:,}
            - Dependents: {client_data['dependents']}
            - Employment: {client_data['employment_status']}
            - Investment Experience: {client_data['investment_experience']}
            
            AVAILABLE HSBC PRODUCTS:
            {products_list}
            
            TASK:
            Analyze this client's profile and provide:
            1. A comprehensive client summary highlighting key insights
            2. 2-3 specific product recommendations with detailed justifications
            
            RESPONSE FORMAT:
            Respond with valid JSON in exactly this format (no markdown, no extra text):
            {response_format}
            
            Ensure recommendations:
            - Match the client's risk profile and goals
            - Avoid products they already have
            - Consider their time horizon and financial capacity
            - Reference specific data points from their profile
            - Include confidence scores between 0.0 and 1.0
            - Prioritize recommendations as "high", "medium", or "low"
            """

    return prompt