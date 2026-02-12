import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Indian Mutual Fund Search",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Indian Mutual Fund Search")
st.write("Search Indian mutual funds using RapidAPI")

# ---------------- USER INPUT ----------------
fund_name = st.text_input(
    "Enter Mutual Fund name (example: SBI, HDFC, ICICI)"
)

# ---------------- BUTTON ACTION ----------------
if st.button("Search Mutual Fund"):

    # 1️⃣ Input validation
    if not fund_name.strip():
        st.warning("Please enter a mutual fund name")

    else:
        with st.spinner("Fetching data..."):

            url = "https://indian-stock-exchange-api2.p.rapidapi.com/mutual_fund_search"

            params = {
                "query": fund_name
            }

            headers = {
                "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com",
                "x-rapidapi-key": st.secrets["RAPID_API_KEY"]  # NEVER hardcode
            }

            response = requests.get(url, headers=headers, params=params)

            # ---------------- DEBUG VISIBILITY ----------------
            st.write("Status Code:", response.status_code)

            # ---------------- RESPONSE HANDLING ----------------
            if response.status_code == 200:
                data = response.json()

                st.write("Raw API Response 👇")
                st.json(data)

                # 🔹 CASE 1: API returns LIST
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    st.success(f"Found {len(df)} mutual funds")
                    st.dataframe(df, use_container_width=True)

                # 🔹 CASE 2: API returns DICT with 'data' key
                elif isinstance(data, dict) and "data" in data and len(data["data"]) > 0:
                    df = pd.DataFrame(data["data"])
                    st.success(f"Found {len(df)} mutual funds")
                    st.dataframe(df, use_container_width=True)

                # 🔹 CASE 3: API returns single DICT
                elif isinstance(data, dict):
                    df = pd.DataFrame([data])
                    st.info("Single record returned")
                    st.dataframe(df, use_container_width=True)

                # 🔹 CASE 4: Empty / unexpected
                else:
                    st.info("No mutual funds found for this search")

            else:
                st.error("API request failed")
                st.write(response.text)