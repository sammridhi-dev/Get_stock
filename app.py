import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
RAPID_API_KEY = os.getenv("RAPID_API_KEY")


def get_stock_data(company_name):

    if not RAPID_API_KEY:
        return "❌ API Key not found in .env file"

    if not company_name.strip():
        return "⚠ Please enter a company name"

    url = "https://indian-stock-exchange-api2.p.rapidapi.com/stock"

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    params = {
        "name": company_name
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"❌ Network/API Error: {str(e)}"

    data = response.json()

    if not data:
        return "⚠ No results found"

    # ✅ If API returns dictionary
    if isinstance(data, dict):

        # Safe extraction for nested values
        risk = data.get("riskMeter", {})
        company_profile = data.get("companyProfile", {})

        result = f"""
## 📊 Stock Details

🔹 **Company:** {data.get('companyName', 'N/A')}  
🔹 **Symbol:** {data.get('symbol', 'N/A')}  
🔹 **Industry:** {data.get('industry', 'N/A')}  
🔹 **Current Price:** {data.get('currentPrice', 'N/A')}  
🔹 **Market Cap:** {data.get('marketCap', 'N/A')}  

---

## 📈 Performance Metrics  

🔹 **1 Day % Change:** {data.get('percentChange', 'N/A')}  
🔹 **52 Week High:** {data.get('yearHigh', 'N/A')}  
🔹 **52 Week Low:** {data.get('yearLow', 'N/A')}  

---

## ⚠️ Risk Analysis  

🔹 **Risk Category:** {risk.get('categoryName', 'N/A')}  
🔹 **Volatility (Std Dev):** {risk.get('stdDev', 'N/A')}  

---

## 📅 Futures & Derivatives  

🔹 **Future Expiry Dates:** {data.get('futureExpiryDates') or "Not Available"}  
🔹 **Future Overview:** {data.get('futureOverviewData') or "Not Available"}  

---

## 💰 Financial Snapshot  

🔹 **Initial Financial Data:** {data.get('initialStockFinancialData') or "Not Available"}  

---

## 🏢 Company Overview  

{company_profile.get('companyDescription', 'N/A')}

---
"""
        return result

    # ✅ If API returns list
    elif isinstance(data, list):

        result = "## 📊 Stock Results\n\n"

        for stock in data:
            result += f"""
🔹 **Company:** {stock.get('companyName', 'N/A')}  
🔹 **Industry:** {stock.get('industry', 'N/A')}  
🔹 **Current Price:** {stock.get('currentPrice', 'N/A')}  

---
"""
        return result

    else:
        return f"❌ Unexpected response format: {data}"


with gr.Blocks(title="Indian Stock Search") as demo:

    gr.Markdown("# 📈 Indian Stock Lookup")
    gr.Markdown("Search by company name (Example: Tata Steel)")

    input_box = gr.Textbox(label="Company Name")
    output = gr.Markdown()
    btn = gr.Button("Search")

    btn.click(
        fn=get_stock_data,
        inputs=input_box,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)