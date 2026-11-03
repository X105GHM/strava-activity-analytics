import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
#import matplotlib.pyplot as plt

#data = {
#    "Name":["Karl"],
#    "Geburtsdataum":["10.09.1955"]}
# erg  = pd.DataFrame(data)



activities = pd.read_csv("./data/activities.csv",sep=",")
measurement = pd.read_csv("./data/measurement_points.csv",sep=",")



st.header("Meine Aktivitäten")
st.dataframe(activities)
st.write("test")


fig = px.bar(
    activities,
    x="sport_type",
    y="weighted_average_watts"

)

##AI generated
df_grouped = activities.groupby("sport_type", as_index=False)["weighted_average_watts"].mean()

fig2 = px.bar(
    df_grouped,
    x="sport_type",
    y="weighted_average_watts",
    title="Durchschnittliche Leistung je Sportart"
)
##



st.plotly_chart(fig)
st.plotly_chart(fig2)

#print(activities.head())
#st.dataframe(activities, use_container_width=True)

# zum rauskopieren
# streamlit run ./spike/matt/app.py