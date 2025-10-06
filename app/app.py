import streamlit as st

# === Настройки страницы ===
st.set_page_config(
    page_title="Steam Swap Account",
    page_icon="🎵",
    #layout="wide"
)

st.title("🎶 (tool)")

url = st.text_input("Put here your steam account", placeholder="...")
