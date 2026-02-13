import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

def get_stock_data(stock_name):

    if not RAPID_API_KEY:
        return "❌ API Key not found. Check your .env file."

    if not stock_name.strip():
        return "⚠ Please enter a stock symbol."

    stock_name = stock_name.upper().strip()

    url = "https://indian-stock-exchange-api2.p.rapidapi.com/mutual_fund_search"

    querystring = {"Indices": "NIFTY 50", "Symbol": stock_name}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"

    if response.status_code != 200:
        return f"❌ API Error {response.status_code}: {response.text}"

    data = response.json()

    if not data:
        return "⚠ No data found for this stock."

    stock = data[0]

    result = f"""
## 📊 STOCK DETAILS

🔹 **Symbol:** {stock.get('symbol', 'N/A')}  
🔹 **Current Price:** ₹ {stock.get('lastPrice', 'N/A')}  
🔹 **Open Price:** ₹ {stock.get('open', 'N/A')}  
🔹 **Day High:** ₹ {stock.get('dayHigh', 'N/A')}  
🔹 **Day Low:** ₹ {stock.get('dayLow', 'N/A')}  
🔹 **Previous Close:** ₹ {stock.get('previousClose', 'N/A')}  
    """

    return result


with gr.Blocks(title="Indian Stock Search") as demo:

    gr.Markdown("# 📊 Indian Stock Search")
    gr.Markdown("Search Indian Stock (Enter NSE Symbol like SBIN, HDFCBANK, TATASTEEL)")

    stock_input = gr.Textbox(label="Enter Stock Symbol")
    output = gr.Markdown()

    search_button = gr.Button("Search Stock")

    search_button.click(
        fn=get_stock_data,
        inputs=stock_input,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share=True)