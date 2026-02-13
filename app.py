import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")


def get_stock_data(company_name):

    if not RAPID_API_KEY:
        return "❌ API Key not found in .env file"

    if not company_name.strip():
        return "⚠ Please enter company name"

    url = "https://indian-stock-exchange-api2.p.rapidapi.com/industry_search"

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    # ✅ FIXED PARAM NAME
    params = {
        "query": company_name   # ✔ API expects 'query'
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"❌ Network/API Error: {str(e)}"

    data = response.json()

    if not isinstance(data, list):
        return f"❌ Unexpected response: {data}"

    if not data:
        return "⚠ No results found"

    result = "## 🔎 Search Results\n\n"

    for stock in data:
        result += f"""
🔹 **Company:** {stock.get('companyName', 'N/A')}  
🔹 **Symbol:** {stock.get('symbol', 'N/A')}  
🔹 **Industry:** {stock.get('industry', 'N/A')}  

---
"""

    return result


with gr.Blocks(title="Indian Stock Search") as demo:

    gr.Markdown("# 📊 Indian Stock Search")
    gr.Markdown("Search by company name (Example: tata steel)")

    input_box = gr.Textbox(label="Company Name")
    output = gr.Markdown()

    btn = gr.Button("Search")

    btn.click(
        fn=get_stock_data,
        inputs=input_box,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()