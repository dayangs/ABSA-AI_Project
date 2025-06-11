import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import get_platform_data

st.set_page_config(page_title="ShopeeFood Review Sentiments", layout="wide", page_icon="🛵")
st.markdown("## 🛵 ShopeeFood Review Sentiments")
st.markdown("Explore what ShopeeFood customers are saying.")

df = get_platform_data("shopeefood")

if df.empty:
    st.warning("No reviews found for ShopeeFood.")
else:
    df.columns = [col.strip().lower() for col in df.columns]

    aspects = [col for col in df.columns if col.endswith("_sentiment")]
    if not aspects:
        st.error("No sentiment columns found.")
    else:
        selected_aspect = st.selectbox("🔍 Select Sentiment Type to Visualize:", aspects, index=aspects.index("review_sentiment") if "review_sentiment" in aspects else 0)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📝 Customer Reviews")
            with st.expander("Click to view full table"):
                display_cols = ['sentence', 'related_ofd', selected_aspect]
                display_cols = [col for col in display_cols if col in df.columns]
                st.dataframe(df[display_cols])

        with col2:
            st.subheader("📊 Sentiment Overview")

            sentiment_counts = df[selected_aspect].value_counts()
            pos = sentiment_counts.get("positive", 0)
            neu = sentiment_counts.get("neutral", 0)
            neg = sentiment_counts.get("negative", 0)
            total = sentiment_counts.sum()

            st.markdown(f"**Total Reviews:** {total}  \n✅ Positive: {pos}  \n⚖️ Neutral: {neu}  \n❌ Negative: {neg}")

            fig, ax = plt.subplots()
            color_map = {"positive": "#4CAF50", "neutral": "#FFC107", "negative": "#F44336"}
            bar_colors = [color_map.get(label.lower(), "gray") for label in sentiment_counts.index]
            sentiment_counts.plot(kind="bar", color=bar_colors, ax=ax)
            ax.set_ylabel("Number of Reviews")
            ax.set_title(f"Overall Sentiment ({selected_aspect.replace('_', ' ').title()})")
            st.pyplot(fig)

    st.markdown("<hr style='border:1px solid #ccc'/>", unsafe_allow_html=True)
    st.caption("Built with 🧡 by Russell Rangers")
