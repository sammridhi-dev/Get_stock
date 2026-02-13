import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

def get_stock_data(stock_name):

    if not stock_name.strip():
        return "⚠ Please enter a stock name."

    url = "https://latest-stock-price.p.rapidapi.com/any"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return "❌ Network error. Please try again."

    if response.status_code != 200:
        return "❌ Failed to fetch stock data."

    data = response.json()

    # Filter stock
    filtered = [
        stock for stock in data
        if stock_name.lower() in stock["symbol"].lower()
    ]

    if not filtered:
        return "⚠ No matching stock found."

    stock = filtered[0]

    # Clean formatted output
    result = f"""
📊 STOCK DETAILS

🔹 Symbol: {stock.get('symbol', 'N/A')}
🔹 Current Price: ₹ {stock.get('lastPrice', 'N/A')}
🔹 Open Price: ₹ {stock.get('open', 'N/A')}
🔹 Day High: ₹ {stock.get('dayHigh', 'N/A')}
🔹 Day Low: ₹ {stock.get('dayLow', 'N/A')}
🔹 Previous Close: ₹ {stock.get('previousClose', 'N/A')}
    """

    return result


# 🎨 Gradio UI
with gr.Blocks(title="Indian Stock Search") as demo:

    gr.Markdown("# 📊 Indian Stock Search")
    gr.Markdown("Search Indian Stock (Secure API Integration)")

    stock_input = gr.Textbox(
        label="Enter Stock Name (Example: SBI, HDFC, ICICI)"
    )

    output = gr.Markdown()

    search_button = gr.Button("Search Stock")

    search_button.click(
        fn=get_stock_data,
        inputs=stock_input,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share=True)