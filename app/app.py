import streamlit as st
from classes import UserVDF
from steam.login_users_vdf_helper import LoginUsersVDF
from config import STEAM_PATH


# Page settings
st.set_page_config(
    page_title="Steam Swap Account",
    page_icon="🎮",
    #layout="wide"
)

# Parse users
accounts = LoginUsersVDF(STEAM_PATH).users

st.title("🎮 Steam Swap Account")
st.caption("Select steam account")

# Selecting account
select_buttons = []

with st.container(horizontal=False, gap="small"):
    for acc in accounts:
        with st.container(border=True, gap="small"):
            cols = st.columns([7, 1], vertical_alignment='center')
            with cols[0]:
                st.write(f"**{acc.PersonaName}** ({acc.AccountName}) - `{acc.SteamID64}`")
            with cols[1]:
                btn = st.button("Select", key=acc.SteamID64)
                select_buttons.append((btn, acc))


# Menu for selected account
for btn in select_buttons:
    btn, acc = btn
    if btn:
        st.markdown("") # little padding
        with st.container(
                horizontal=False,
                gap="small",
                horizontal_alignment="distribute",
        ):

            st.subheader(f"✅ Selected account: **{acc.PersonaName}**")

            cols_btn = st.columns(3)
            with cols_btn[0]:
                if st.button("🔗 Make Shortcut"):
                    st.success(f"Shortcut created for {acc.AccountName}")
            with cols_btn[1]:
                if st.button("🗑️ Remove Shortcut"):
                    st.warning(f"Shortcut removed for {acc.AccountName}")
            with cols_btn[2]:
                if st.button("ℹ️ Show Details"):
                    st.json(acc.__dict__)

            break
else:
    st.info("Select account to continue.")