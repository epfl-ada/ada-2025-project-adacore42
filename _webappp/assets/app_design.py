import streamlit as st

st.markdown(
    """
    <style>
    p {
        text-align: justify;
        text-justify: inter-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    li {
        text-align: justify;
        text-justify: inter-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)



        




st.markdown(
    """
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        padding: 10px 10px;
        border-radius: 10px;
        border: none;
        width: 100%;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)




st.markdown("""
<style>
div[data-testid="stAlert"] {
    background-color: rgba(76, 175, 80, 0.12);  /* vert clair transparent */
    border-left: 6px solid #4CAF50;            /* bande verte */
    color: #333333;                            /* texte gris foncé */
}

div[data-testid="stAlert"] svg {
    color: #333333;                            /* icône verte */
}
</style>
""", unsafe_allow_html=True)






# st.markdown(
#     """
#     <style>
#     .titleButton button {
#         background: linear-gradient(135deg, #4CAF50, #2e7d32);
#         color: white;
#         font-size: 28px;
#         font-weight: 700;
#         padding: 18px 36px;
#         border-radius: 14px;
#         border: none;
#         width: 100%;
#         letter-spacing: 0.5px;
#     }

#     .titleButton button:hover {
#         background: linear-gradient(135deg, #45a049, #256628);
#         transform: scale(1.02);
#     }

#     .titleButton button:active {
#         transform: scale(0.98);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )