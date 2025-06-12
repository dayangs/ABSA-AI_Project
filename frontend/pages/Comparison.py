import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import get_platform_data

st.set_page_config(page_title="Platform Sentiment Comparison", layout="wide")
st.markdown("## 📊 Sentiment Comparison Across Platforms")
st.markdown("Compare overall customer sentiment for GrabFood, ShopeeFood, and PandaFood.")

# Load and clean data
platforms = {
    "GrabFood": "grabfood",
    "ShopeeFood": "shopeefood",
    "PandaFood": "foodpanda"
}

sentiment_summary = {}

for name, keyword in platforms.items():
    df = get_platform_data(keyword)
    df.columns = [col.strip().lower() for col in df.columns]
    if "review_sentiment" in df.columns:
        sentiment_counts = df["review_sentiment"].value_counts()
        sentiment_summary[name] = sentiment_counts

# Merge into a DataFrame
summary_df = pd.DataFrame(sentiment_summary).fillna(0).astype(int)

if summary_df.empty:
    st.warning("Sentiment data not available for any platform.")
else:
    st.subheader("📦 Review Sentiment Distribution")
    st.dataframe(summary_df)

    # Plot
    st.subheader("📈 Sentiment Comparison Chart")
    fig, ax = plt.subplots(figsize=(8, 5))
    summary_df.T.plot(kind='bar', ax=ax)
    ax.set_ylabel("Number of Reviews")
    ax.set_xlabel("Platform")
    ax.set_title("Review Sentiment by Platform")
    ax.legend(title="Sentiment")
    st.pyplot(fig)

# Footer Section      
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; font-size: 13px; color: gray;'>
        ⚠ This dashboard is for academic use only. Sentiment analysis is auto-generated and may not reflect actual customer intentions. Use with care.<br><br>
        Built with 💙 by Russell Rangers
    </div>
    """,
    unsafe_allow_html=True
)