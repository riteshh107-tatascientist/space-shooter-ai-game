import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Game Dashboard", layout="centered")

st.title("🎮 Game Analytics Dashboard")

# Check file
if not os.path.exists("game_data.csv"):
    st.warning("No data yet! Play the game first.")
    st.stop()

# Load data ONCE (FIXED)
@st.cache_data
def load_data():
    df = pd.read_csv("game_data.csv", header=None)

    # Ensure correct columns
    if df.shape[1] == 4:
        df.columns = ["score", "level", "lives", "time"]
    else:
        st.error("CSV format incorrect!")
        st.stop()

    return df

df = load_data()

if df.empty:
    st.warning("CSV is empty!")
    st.stop()

st.dataframe(df)

# 📈 Score Trend
st.subheader("Score Trend")
fig1, ax1 = plt.subplots()
ax1.plot(df["score"])
ax1.set_xlabel("Game Sessions")
ax1.set_ylabel("Score")
ax1.set_title("Score Over Time")
st.pyplot(fig1)

# 📊 Level vs Score
st.subheader("Level vs Score")
fig2, ax2 = plt.subplots()
ax2.scatter(df["level"], df["score"])
ax2.set_xlabel("Level")
ax2.set_ylabel("Score")
ax2.set_title("Level vs Score")
st.pyplot(fig2)

# 📊 Stats
st.subheader("Statistics")
st.write("Average Score:", df["score"].mean())
st.write("Max Score:", df["score"].max())
st.write("Total Games:", len(df))