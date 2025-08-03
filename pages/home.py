import streamlit as st
from utils.config import load_config
from components.number_field import st_create_number_field
import pandas as pd
import services.providers as providers


@st.cache_resource
def load_config_with_cache():
    return load_config()


def page():
    st.set_page_config(
        page_title="USD Calculator",
        page_icon="💵",
        layout="centered",
        initial_sidebar_state="auto",
    )

    config = load_config_with_cache()

    st.title("USD Calculator", width="content")
    st.warning(
        "⚠️ Recuerda que los valores de tasas y costos son aproximados y pueden variar."
        "\n\n"
        "Valores que superen 65 UVT (aproximadamente 3.2 millones COP) están sujetos a GMF (4x1000)."
        "\n\n"
        "Marca la casilla de GMF si deseas incluir este impuesto en el cálculo."
    )

    if "amount" not in st.session_state:
        st.session_state.amount = 3000.0
    if "flow" not in st.session_state:
        st.session_state.flow = "Global66 directo"
    if "operation" not in st.session_state:
        st.session_state.operation = "Conversion USD a COP"
    if "result" not in st.session_state:
        st.session_state.result = False

    st.session_state.flow = st.selectbox("Selecciona el proveedor:", ["Global66", "Schwab + Remitly"])
    st.session_state.operation = st.selectbox(
        "Selecciona el tipo de operación:",
        options=["Conversion USD a COP", "Enviar USD a USD", "Enviar COP a COP"],
        index=["Conversion USD a COP", "Enviar USD a USD", "Enviar COP a COP"].index(st.session_state.operation),
    )

    if st.session_state.flow == "Global66" and st.session_state.operation == "Conversion USD a COP":
        st.session_state.amount = st_create_number_field(
            "💵 Ingresar monto en USD a procesar:",
            value=st.session_state.amount,
        )

    if st.session_state.flow == "Global66" and st.session_state.operation == "Enviar USD a USD":
        st.session_state.amount = st_create_number_field(
            "💵 Ingresar monto en USD a procesar:",
            value=st.session_state.amount,
        )

    if st.session_state.flow == "Global66" and st.session_state.operation == "Enviar COP a COP":
        st.session_state.amount = st_create_number_field(
            "💵 Ingresar monto en COP a procesar:",
            value=st.session_state.amount,
        )

    if st.button("Calculate", icon="🧮", use_container_width=True) or st.session_state.result:
        if st.session_state.flow == "Global66":
            calculator = providers.Global66(config)
            result = calculator.calculate(operation=st.session_state.operation, amount=st.session_state.amount)
        elif st.session_state.flow == "Schwab + Remitly":
            calculator = providers.Remitly(config)
            result = calculator.calculate(operation=st.session_state.operation, amount=st.session_state.amount)
        else:
            result = pd.DataFrame()
        if "resumen" not in st.session_state:
            st.session_state.resumen = calculator.get_summary()
        st.subheader("Rates and Fees summary")
        st.dataframe(st.session_state.resumen, hide_index=True)
        st.subheader("Results: Global66")
        st.dataframe(result, hide_index=True)
        st.session_state.result = True
