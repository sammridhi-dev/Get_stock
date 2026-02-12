import streamlit as st
import requests
import pandas as pd

# Page config
st.set_page_config(
    page_title="Indian Mutual Fund Search",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Indian Mutual Fund Search")
st.write("Search Indian mutual funds using RapidAPI")

# User input
fund_name = st.text_input(
    "Enter Mutual Fund name (example: SBI, HDFC, ICICI)"
)

# Button
if st.button("Search Mutual Fund"):
    if not fund_name.strip():
        st.warning("Please enter a mutual fund name")
    else:
        with st.spinner("Fetching data..."):

            url = "https://indian-stock-exchange-api2.p.rapidapi.com/mutual_fund_search"

            querystring = {
                "query": fund_name
            }

            headers = {
                "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
                "x-rapidapi-key": st.secrets["RAPID_API_KEY"]
            }

            response = requests.get(
                url,
                headers=headers,
                params=querystring
            )

            if response.status_code == 200:
                data = response.json()

                # Defensive check (API responses vary)
                if isinstance(data, dict) and "data" in data and len(data["data"]) > 0:
                    df = pd.DataFrame(data["data"])

                    st.success(f"Found {len(df)} mutual funds")
                    st.dataframe(df, use_container_width=True)

                else:
                    st.info("No mutual funds found for this search")

            else:
                st.error(f"API Error: {response.status_code}")