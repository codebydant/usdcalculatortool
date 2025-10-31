import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from providers import PROVIDERS
from services import SERVICES
from components import number_field, options
from utils.config import load_config


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

    st.title("USD Calculator")
    st.warning(
        "⚠️ Recuerda que los valores de tasas y costos son aproximados y pueden variar."
        "\n\n"
        "Valores que superen 65 UVT (~3.2M COP) están sujetos a GMF (4x1000)."
        "\n\n"
    )

    # Initialize session state
    default_state = {
        "amount": 3000.0,
        "operation": None,
        "provider": None,
        "result": None,
        "currency_from": "USD",
        "currency_to": "COP",
    }
    for key, val in default_state.items():
        st.session_state.setdefault(key, val)

    with stylable_container(
        "calculator_container",
        css_styles="""
        {
            background-color: rgba(46, 204, 113, 0.18);
            border: 3px solid black;
            border-radius: 30px;
            # padding: 20px;
            height: 650px;
            overflow-y: auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 480px;

            .stMainBlockContainer {
                center-align: center;
            }

            .stForm {
                align-items: center;
                justify-content: center;
            }

            .stVerticalBlock {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }

            .stElementContainer{
                width: 300px;
            }

            .stRadio {
                width: 280px;
            }

            .stSelectbox input {
                pointer-events: none;
                caret-color: transparent;
                user-select: none;
                cursor: default !important;
            }

            .stSelectbox * {
                cursor: default !important;
            }

            .stAlert{
                width: 400px;
            }
        }
        """,
    ):
        with st.form("calculator_form", clear_on_submit=False):
            number_field.st_create_number_field("Cantidad:", st.session_state.amount)
            provider_names = list(PROVIDERS.keys())
            services_names = list(SERVICES.keys())
            options.st_create_options_field(provider_names, services_names)
            submitted = st.form_submit_button("Calculate", icon="🧮", use_container_width=True)

        if submitted:
            try:
                config = load_config_with_cache()

                service = SERVICES[st.session_state.operation]
                provider = PROVIDERS[st.session_state.provider]

                result = service.run(
                    config=config,
                    provider=provider,
                    amount=st.session_state.amount,
                    currency_from=st.session_state.currency_from,
                    currency_to=st.session_state.currency_to,
                )

                st.session_state.result = result

            except NotImplementedError as e:
                st.error(f"Error: {e}")
            except ValueError as e:
                st.error(f"Error: {e}")

    if st.session_state.get("result") is not None:
        st.subheader(f"Results: {st.session_state.provider}")
        st.dataframe(st.session_state.result, hide_index=True)
