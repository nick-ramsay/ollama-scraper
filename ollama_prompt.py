import requests
import json
import sys


def llm_analysis(stock_data: dict) -> str:
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""Provide a short, one to two paragraph summary of your thoughts on this investment. The opening sentence should introduce the company with it's name and the ticker symbol. Don't be too technical. Finish your summary with a simple sentence containing a recommendation of whether to buy, hold, or sell the stock. The sentence should begin with 'In my current opinion, this is a [STRONG BUY, BUY, HOLD, SELL, or STRONG SELL].'
      Here is the stock data in a dictionary format:

    {json.dumps(stock_data, indent=2)}

    """

    payload = {
        "model": "gpt-oss:20b",
        "prompt": prompt,
        "stream": False,
        "temperature": 0,
        "system": "You are an investment analyst.You are given a dictionary of stock fundamentals and you need to provide a brief analysis of the key metrics and any notable observations."
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response received")
    except requests.exceptions.RequestException as e:
        return f"Error calling Ollama: {e}"