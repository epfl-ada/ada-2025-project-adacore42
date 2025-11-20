import streamlit as st

def render():
    
    st.title("📐 Layout Demonstration")

    layout_tabs = st.tabs(["Tabs", "Columns", "Containers", "Expanders"])

    # -----------------------
    # Tabs inside Tabs
    # -----------------------
    with layout_tabs[0]:
        st.subheader("Nested Tabs Example")

        nested_tab1, nested_tab2 = st.tabs(["Numbers", "Text"])

        with nested_tab1:
            st.write("Nested tab displaying numbers:")
            st.write(list(range(1, 6)))

        with nested_tab2:
            st.write("Nested tab displaying text:")
            st.write("Hello from nested tabs!")

    # -----------------------
    # Columns
    # -----------------------
    with layout_tabs[1]:
        st.subheader("Column Layouts")

        col1, col2, col3 = st.columns(3)
        col1.metric("Speed", "120 km/h", "+10")
        col2.metric("Temperature", "21°C", "-2")
        col3.metric("Load", "68%", "+13%")

        st.caption("Metrics presented using the native `metric` component.")

    # -----------------------
    # Containers
    # -----------------------
    with layout_tabs[2]:
        st.subheader("Container Example")

        with st.container():
            st.write("This is inside a container.")
            inner_col1, inner_col2 = st.columns(2)
            inner_col1.write("Left section")
            inner_col2.write("Right section")

        st.write("This is outside the container.")

    # -----------------------
    # Expanders
    # -----------------------
    with layout_tabs[3]:
        st.subheader("Expander Example")

        with st.expander("Click me!"):
            st.write("Useful for long documentation or settings sections.")

