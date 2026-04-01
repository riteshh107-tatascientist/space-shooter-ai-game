import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎮 Game Analytics Dashboard")

try:
    df = pd.read_csv("game_data.csv")
except:
    st.warning("No data yet! Play the game first.")
    st.stop()

st.dataframe(df)

st.subheader("Score Trend")
plt.plot(df["score"])
st.pyplot(plt)

st.subheader("Level vs Score")
plt.scatter(df["level"], df["score"])
st.pyplot(plt)

st.write("Average Score:", df["score"].mean())