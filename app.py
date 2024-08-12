import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

#st.title("Hello World!")
#st.markdown("## My first streamlit application dashboard!")

DATA_URL = (
"/home/rhyme/Desktop/Project/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor vehicle collisions New York City")
st.markdown("This application is a streamlit dashboard that can be used "
"to analize motor vehicle collision in NYC Ã°ÂÂÂ¥Ã°ÂÂÂ")
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH_DATE", "CRASH_TIME"]])
    data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash_date_crash_time": "date/time"}, inplace=True)
    return data

data = load_data(10000)
original_data = data

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))


st.header("How many collisions occur during a given time of a day")
#hour = st.selectbox("Hour to lloak at", range(0, 24), 1)  dropdpwn menue
hour = st.slider("Hour to lloak at", 0, 24 )
data = data[data["date/time"].dt.hour == hour]


st.markdown("Vehicle collisions between %i:00 and %i:00" %(hour, (hour + 1)% 24))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude": midpoint[1],
        "zoom":11,