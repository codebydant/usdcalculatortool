import streamlit as st


def st_create_options_field(providers_list, services_list):
    st.session_state.provider = st.selectbox(
        "Selecciona el proveedor:",
        options=providers_list,
        index=providers_list.index(st.session_state.provider) if st.session_state.provider else 0,
        key="provider_select",
    )

    st.session_state.operation = st.selectbox(
        "Selecciona el tipo de operación:",
        options=services_list,
        index=services_list.index(st.session_state.operation) if st.session_state.operation else 0,
        key="operation_select",
    )

    st.session_state.currency_from = st.radio(
        "Selecciona la moneda de origen:",
        options=["USD", "COP"],
        index=0 if st.session_state.currency_from == "USD" else 1,
        key="currency_from_select",
    )

    st.session_state.currency_to = st.radio(
        "Selecciona la moneda de destino:",
        options=["COP", "USD"],
        index=0 if st.session_state.currency_to == "COP" else 1,
        key="currency_to_select",
    )
