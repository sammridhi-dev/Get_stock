# app.py

import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Indian Stock Search",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Indian Stock Search")
st.write("Search Indian Stock (Backend Secured API)")

stock_name = st.text_input(
    "Enter Stock name (example: SBI, HDFC, ICICI)"
)

if st.button("Search Stock"):

    if not stock_name.strip():
        st.warning("Please enter a stock name")

    else:
        with st.spinner("Fetching data..."):

            backend_url = "http://127.0.0.1:8000/stock"

            response = requests.get(
                backend_url,
                params={"name": stock_name}
            )

            if response.status_code == 200:

                data = response.json()

                if not data:
                    st.warning("No stock found.")
                    st.stop()

                # Convert to DataFrame
                df = pd.DataFrame(data)

                # ✅ Keep only important columns (edit based on API response)
                important_columns = [
                    "symbol",
                    "lastPrice",
                    "open",
                    "dayHigh",
                    "dayLow"
                ]

                available_cols = [col for col in important_columns if col in df.columns]
                df = df[available_cols]

                # ✅ Rename columns for clean display
                df = df.rename(columns={
                    "symbol": "Stock",
                    "lastPrice": "Current Price",
                    "open": "Open Price",
                    "dayHigh": "Day High",
                    "dayLow": "Day Low"
                })

                # ✅ Format numeric columns
                for col in df.columns:
                    if col != "Stock":
                        df[col] = df[col].astype(float).round(2)

                st.success("Data fetched successfully ✅")

                # ✅ Show top stock as metric
                first_stock = df.iloc[0]

                col1, col2, col3 = st.columns(3)

                col1.metric("Stock", first_stock["Stock"])
                col2.metric("Current Price", f"₹ {first_stock['Current Price']}")
                col3.metric("Day High", f"₹ {first_stock['Day High']}")

                st.divider()

                # ✅ Show clean table
                st.subheader("Stock Details")
                st.dataframe(df, use_container_width=True)

            else:
                st.error("Backend request failed")
                st.write(response.text)