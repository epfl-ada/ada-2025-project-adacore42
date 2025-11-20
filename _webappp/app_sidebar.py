import streamlit as st

def render():
    st.title("🔧 Controls")

    st.write("This sidebar uses only native elements.")

    st.subheader("Quick Actions")

    if st.button("Reset Counter"):
        st.session_state.counter = 0
        st.success("Counter reset!")

    st.subheader("Filters")
    st.radio("Category", ["A", "B", "C"])
    st.slider("Threshold", 0, 100, 30)

    st.divider()
    st.write("Everything here is 100% native Streamlit.")