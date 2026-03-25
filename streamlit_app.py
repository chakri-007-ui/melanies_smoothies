# -------------------------------
# IMPORT LIBRARIES
# -------------------------------
import streamlit as st
import requests
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smoothie App", layout="wide")

# -------------------------------
# UI HEADER
# -------------------------------
st.title('🍹 Customize Your Smoothie')
st.write("Choose up to 5 fruits for your smoothie!")

# -------------------------------
# USER INPUT
# -------------------------------
name_on_order = st.text_input('Name on Smoothie:')

# -------------------------------
# SNOWFLAKE CONNECTION
# -------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -------------------------------
# FETCH DATA FROM SNOWFLAKE
# -------------------------------
@st.cache_data
def load_fruit_data():
    query = "SELECT FRUIT_NAME, SEARCH_ON FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
    return session.sql(query).to_pandas()

pd_df = load_fruit_data()

# Convert to list
fruit_list = pd_df["FRUIT_NAME"].tolist()

# -------------------------------
# MULTISELECT INPUT
# -------------------------------
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# -------------------------------
# CACHE API CALL (FASTER)
# -------------------------------
@st.cache_data(show_spinner=False)
def get_fruit_data(search_on):
    url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# -------------------------------
# PROCESS SELECTED FRUITS
# -------------------------------
if ingredients_list:

    # Show selected ingredients
    st.write("### 🥗 Selected Ingredients:")
    st.write(ingredients_list)

    # Price Calculation
    price = len(ingredients_list) * 50
    st.write(f"💰 Total Price: ₹{price}")

    ingredients_string = ", ".join(ingredients_list)

    for fruit_chosen in ingredients_list:

        # Get SEARCH_ON value
        try:
            search_on = pd_df.loc[
                pd_df['FRUIT_NAME'] == fruit_chosen,
                'SEARCH_ON'
            ].iloc[0]

        except:
            st.error(f"Search value not found for {fruit_chosen}")
            continue

        # UI Section
        st.markdown("---")
        st.subheader(f"🍎 {fruit_chosen} Nutrition Information")

        # API Call with Spinner
        with st.spinner(f"Fetching {fruit_chosen} data..."):

            try:
                data = get_fruit_data(search_on)

                if data:
                    df_api = pd.json_normalize(data)
                    st.dataframe(df_api, use_container_width=True)
                else:
                    st.warning(f"{fruit_chosen} not found in API")

            except Exception as e:
                st.error(f"Error fetching data for {fruit_chosen}")

    # -------------------------------
    # SUBMIT ORDER
    # -------------------------------
    if st.button('✅ Submit Order'):

        # Validation
        if not name_on_order:
            st.warning("⚠️ Please enter your name before ordering.")
        else:
            try:
                # Secure Insert (Prevents SQL Injection)
                session.sql(
                    """
                    INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                    (ingredients, name_on_order, order_time)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    """,
                    params=[ingredients_string, name_on_order]
                ).collect()

                st.success('🎉 Your smoothie has been ordered!')

            except Exception as e:
                st.error("❌ Failed to insert order")
