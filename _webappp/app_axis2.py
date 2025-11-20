import streamlit as st

def render():
        
    st.title("⚙ Settings")

    st.write("All inputs below are native Streamlit widgets.")

    with st.form("settings_form"):
        username = st.text_input("Username")
        theme_choice = st.radio("Theme", ["Light", "Dark", "System"])
        volume = st.slider("Volume", 0, 100, 50)

        submitted = st.form_submit_button("Save Settings")
        if submitted:
            st.success(f"Settings saved for **{username}**!")

    st.divider()

    st.subheader("Toggle Options")
    st.checkbox("Enable notifications")
    st.checkbox("Enable autosave")
