import streamlit as st
from streamlit_geolocation import streamlit_geolocation

from utils.api import get_weather_ai_advisory


def render_weather_alert():

    with st.expander("🌦️ AI Weather Health Advisory", expanded=True):

        location = streamlit_geolocation()

        if not location or not location.get("latitude"):

            st.info(
                "Allow location permission to receive AI-based weather health warnings."
            )

            return

        response = get_weather_ai_advisory(
            st.session_state.token,
            location["latitude"],
            location["longitude"]
        )

        if response.status_code == 200:

            data = response.json()

            c1, c2 = st.columns(2)
            st.markdown(
    f"""
    ### 📍 {data.get('location')},
    {data.get('state')},
    {data.get('country')}
    """
)
            st.caption(
    f"""
    Latitude: {data.get('latitude')} |
    Longitude: {data.get('longitude')}
    """
)
            with c1:
                st.metric(
                    "Temperature",
                    f"{data.get('temperature')} °C"
                )

            with c2:
                st.metric(
                    "Humidity",
                    f"{data.get('humidity')}%"
                )

            st.warning(
                data.get(
                    "ai_advisory",
                    "No advisory available."
                )
            )

        else:

            st.info(
                "Weather advisory currently unavailable."
            )