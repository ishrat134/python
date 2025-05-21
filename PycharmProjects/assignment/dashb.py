def render_login_screen() -> None:
    """Render the login screen with Microsoft SSO."""
    # 1. FIRST CHECK - Handle post-authentication redirect
    if st.session_state.get("auth_redirect", False):
        st.session_state.auth_redirect = False
        if st.session_state.get("authenticated", False):
            # Use the new navigation API in Streamlit >= 1.27
            if hasattr(st, "switch_page"):
                st.switch_page("pages/dashboard.py")  # or your home page filename
            else:
                st.experimental_rerun()
        return

    # 2. SECOND CHECK - Already authenticated
    if st.session_state.get("authenticated", False):
        if not is_token_valid():
            logger.info("Access token expired, redirecting to login")
            st.session_state.authenticated = False
        else:
            if st.query_params.get("code"):
                st.query_params.clear()
            return  # Let the main app redirect to home page

    # [Rest of your existing login UI code...]
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("src/dashboards/logo.png", width=80)
    # ... etc ...

    # 3. In your successful authentication block:
    if token_result and "access_token" in token_result:
        # [Your existing user setup code...]
        
        # After all successful auth setup:
        st.session_state.authenticated = True
        st.session_state.auth_redirect = True  # Set the redirect flag
        st.query_params.clear()
        
        # Force immediate redirect
        if hasattr(st, "switch_page"):
            st.switch_page("pages/dashboard.py")
        else:
            st.experimental_rerun()
        return
