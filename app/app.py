import streamlit as st
import utils
from steam.login_users_vdf_helper import LoginUsersVDF
from classes import UserVDF
from config import STEAM_PATH


# Page settings
st.set_page_config(
    page_title="Steam Swap Account",
    page_icon="🎮"
)

# Parse users
accounts = LoginUsersVDF(STEAM_PATH).users

st.title("🎮 Steam Swap Account")
st.caption("Select steam account")

# Initialize session
if "selected_acc" not in st.session_state:
    st.session_state.selected_acc = None

# Selecting account
for acc in accounts:
    with st.container(border=True, gap="small"):
        cols = st.columns([5, 2, 1], vertical_alignment='center')
        with cols[0]:
            st.write(f"**{acc.PersonaName}** ({acc.AccountName}) - `{acc.SteamID64}`")
            st.json(acc.todict(), expanded=False)

        with cols[2]:
            if st.button("Select", key=acc.SteamID64):
                st.session_state.selected_acc = acc
                with cols[1]:
                    st.success(f"Selected {acc.PersonaName}")

# Menu for selected account
acc = st.session_state.selected_acc

if acc:
    st.markdown("")
    st.subheader(f"⚙️ Actions with Selected account")

    cols_btn = st.columns(4)
    with cols_btn[0]:
        if st.button("🔗 Make Shortcut"):
            utils.create_steam_login_shortcut(
                steam_id64=acc.SteamID64,
                username=acc.AccountName,
                script_path=utils.get_desktop_path(
                    filename=f"{acc.AccountName}.ps1"
                )
            )
            st.session_state.selected_acc = None
            st.success(f"Shortcut created on desktop for {acc.AccountName}")

    with cols_btn[1]:
        if st.button("⛓️‍💥 Clear selected"):
            st.session_state.selected_acc = None
            st.rerun()
else:
    st.info("Select account to continue.")
