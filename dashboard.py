import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎮 Game Analytics Dashboard")

# Safe loading
try:
    df = pd.read_csv("game_data.csv")
except:
    st.warning("No data yet! Play the game first.")
    st.stop()

# Agar file empty ho
if df.empty:
    st.warning("CSV file is empty!")
    st.stop()

st.dataframe(df)

# Score Trend
st.subheader("Score Trend")
fig1, ax1 = plt.subplots()
ax1.plot(df["score"])
st.pyplot(fig1)

# Level vs Score
st.subheader("Level vs Score")
fig2, ax2 = plt.subplots()
ax2.scatter(df["level"], df["score"])
st.pyplot(fig2)

# Stats
st.subheader("Statistics")
st.write("Average Score:", df["score"].mean())
st.write("Max Score:", df["score"].max())