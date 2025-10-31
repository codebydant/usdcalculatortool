import streamlit as st


def st_create_number_field(message: str, value: float):
    st.session_state.amount = st.number_input(message, min_value=1.0, max_value=1e12, value=value, format="%0.f")
