
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

st.set_page_config(layout="wide")
st.title("📈 Realtime BTC High Price × Combined Upscore")

csv_price = "btc_2024_to_last.csv"
csv_score = "sigma_sell.csv"

def plot_dual_axis_chart():
    if not os.path.exists(csv_price) or not os.path.exists(csv_score):
        st.warning("CSVファイルが見つかりません。")
        return

    df_price = pd.read_csv(csv_price, parse_dates=["open_time"])
    df_score = pd.read_csv(csv_score, parse_dates=["open_time"])

    df_merged = pd.merge(df_price, df_score[["open_time", "combined_upscore"]], on="open_time", how="inner")
    df_merged = df_merged.tail(100)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Combined Upscore", color="blue")
    ax1.plot(df_merged["open_time"], df_merged["combined_upscore"], color="blue", label="Combined Upscore")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("BTC High Price", color="red")
    ax2.plot(df_merged["open_time"], df_merged["high"], color="red", alpha=0.6, label="High Price")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()

    plt.title("BTC High vs Combined Upscore (Latest 100)")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

refresh_interval = 60
countdown = st.empty()

plot_dual_axis_chart()

for i in range(refresh_interval, 0, -1):
    countdown.markdown(f"⏳ 自動更新まで: **{i}** 秒")
    time.sleep(1)
    if i == 1:
        st.rerun()
