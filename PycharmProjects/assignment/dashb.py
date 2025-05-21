import streamlit as st
import time
import json
from pathlib import Path
from typing import Optional
from your_config_module import UserConfig  # Replace with your actual config module
from your_auth_module import initialize_msal_app, acquire_access_token, fetch_user_data  # Replace with your auth module

# Configuration
CONFIG_FILE = Path("config/users.json")
REDIRECT_URL = "https://your-redirect-url.com"  # Replace with your actual redirect URL
SCOPES = ["User.Read"]  # Your required MS Graph permissions

def load_config() -> Optional[UserConfig]:
    """Load the user configuration file"""
    try:
        if not CONFIG_FILE.exists():
            return UserConfig(root={})
        
        with open(CONFIG_FILE, "r") as f:
            config_dict = json.load(f)
            return UserConfig(root=config_dict)
            
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return None

def save_config(config: UserConfig) -> bool:
    """Save the user configuration file"""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {k: v.model_dump() for k, v in config.root.items()}
        
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_dict, f, indent=2, default=str)
            
        return True
    except Exception as e:
        st.error(f"Error saving configuration: {e}")
        return False

def is_token_valid() -> bool:
    """Check if the stored token is still valid"""
    # Implement your token validation logic
    return True  # Replace with actual validation

def render_login_screen() -> None:
    """Render the login screen with Microsoft SSO"""
    # 1. Redirect check - must be first in function
    if st.session_state.get("auth_redirect", False):
        st.session_state.auth_redirect = False
        if st.session_state.get("authenticated", False):
            if hasattr(st, "switch_page"):
                st.switch_page("pages/dashboard.py")  # Your home page
            else:
                st.experimental_rerun()
        return

    # 2. Already authenticated check
    if st.session_state.get("authenticated", False):
        if not is_token_valid():
            st.session_state.authenticated = False
        else:
            if st.query_params.get("code"):
                st.query_params.clear()
            return  # Main app will handle redirect

    # 3. Render login UI
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("src/dashboards/logo.png", width=80)
    with col2:
        st.title("MCP Management Dashboard")
    st.divider()

    # 4. Process authentication
    if st.query_params.get("code"):
        process_authentication()

    # 5. Show login button if not authenticated
    if not st.session_state.get("authenticated", False):
        show_login_button()

def process_authentication() -> None:
    """Handle the authentication flow"""
    app = initialize_msal_app()
    auth_code = st.query_params.get("code")
    token_result = acquire_access_token(app, auth_code)

    if token_result and "access_token" in token_result:
        save_token_to_session(token_result)
        user_data = fetch_user_data(token_result["access_token"])

        if user_data and "id" in user_data:
            handle_user_data(user_data)
            
            # Set redirect flag and perform immediate redirect
            st.session_state.auth_redirect = True
            if hasattr(st, "switch_page"):
                st.switch_page("pages/dashboard.py")
            else:
                st.experimental_rerun()
            return

    st.error("Authentication failed. Please try again.")
    st.query_params.clear()

def handle_user_data(user_data: dict) -> None:
    """Process and store user data"""
    ms_user_id = user_data["id"]
    email = user_data.get("mail", "")
    full_name = user_data.get("displayName", "")

    users_config = load_config()
    if not users_config:
        st.error("Failed to load user configuration")
        return

    # Create new user if needed
    if ms_user_id not in users_config.root and email:
        users_config.create_user(
            user_key=ms_user_id,
            full_name=full_name,
            email=email,
            job_title=user_data.get("jobTitle", ""),
            location=user_data.get("officeLocation", ""),
            phone=user_data.get("businessPhones", [""])[0],
        )
        if not save_config(users_config):
            return

    # Update session state
    st.session_state.authenticated = True
    st.session_state.username = ms_user_id
    st.session_state.display_name = full_name
    st.session_state.user_data = users_config.root.get(ms_user_id, {})

def show_login_button() -> None:
    """Display Microsoft login button"""
    app = initialize_msal_app()
    auth_url = app.get_authorization_request_url(SCOPES, redirect_url=REDIRECT_URL)
    
    st.subheader("Login with Microsoft")
    st.markdown(f"""
    <div style="text-align: center; margin: 3em 0;">
        <a href="{auth_url}">
            <img src="https://learn.microsoft.com/en-us/azure/active-directory/develop/media/howto-add-branding-in-apps/ms-symbollockup_signin_light.png" 
                 alt="Sign in with Microsoft" 
                 style="height: 41px; width: 215px;"/>
        </a>
    </div>
    """, unsafe_allow_html=True)

def save_token_to_session(token_result: dict) -> None:
    """Store token in session state"""
    st.session_state.token = token_result
    st.session_state.token_expires = time.time() + token_result.get("expires_in", 0)
