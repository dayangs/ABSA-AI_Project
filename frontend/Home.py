#run >> python -m streamlit run Home.py
import streamlit as st
import base64
import matplotlib.pyplot as plt
import pandas as pd
from model import get_platform_data
from wordcloud import WordCloud

st.set_page_config(page_title="ABSA Food Dashboard", layout="wide", page_icon="🍽️")

st.markdown("<h1 style='text-align: center;'>🍽️ ABSA for Online Food Delivery Reviews</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Welcome to the Malaysian Sentiment Intelligence Dashboard</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

import pandas as pd

# Load dataset (if not already loaded in Home.py)
@st.cache_data
def load_absa_results():
    df = pd.read_excel("frontend/absa_ModelResults.xlsx")
    df.columns = [c.strip().lower() for c in df.columns]
    return df

df = load_absa_results()

# CSS for card layout and fixed icon sizing
st.markdown("""
    <style>
        .card-container {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
        }
        .card {
            background-color: #e8f5ff;
            border-radius: 15px;
            padding: 1.5rem;
            width: 260px;
            text-align: center;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            transition: 0.3s ease;
            cursor: pointer;
            color: #0d1117;
        }
        .card:hover {
            background-color: #f1f5ff;
            transform: scale(1.03);
        }
        .icon-img {
            height: 100px;
            width: 100px;
            object-fit: contain;
            margin-bottom: 10px;
            padding: 10px;
            background-color: white;
            border-radius: 12px;
            box-sizing: border-box;
        }
        a.card-link {
            text-decoration: none;
            color: inherit;
        }
        .rank-section {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-width: 500px;
            margin: auto;
            font-family: 'Segoe UI', sans-serif;
        }
        
        .rank-row {
            display: flex;
            justify-content: space-between;
            padding: 0.8rem 1rem;;
            background-color:  #f6f9ff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        }
        .rank-name {
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
        }
            
    </style>
""", unsafe_allow_html=True)

# Load and encode each logo
def load_img_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

grab_logo = load_img_as_base64("frontend/images/grab.png")
shopee_logo = load_img_as_base64("frontend/images/shopee.png")
panda_logo = load_img_as_base64("frontend/images/panda.png")

# Display cards with logos
st.markdown(f"""
<div class="card-container">

  <a href="/Shopeefood" class="card-link">
    <div class="card">
      <img src="data:image/png;base64,{shopee_logo}" class="icon-img">
      <h3>ShopeeFood</h3>
      <p>Fast deliveries, deals, and user feedback from ShopeeFood users.</p>
    </div>
  </a>

  <a href="/Grabfood" class="card-link">
    <div class="card">
      <img src="data:image/png;base64,{grab_logo}" class="icon-img">
      <h3>GrabFood</h3>
      <p>Explore pricing, speed, and user sentiment from GrabFood reviews.</p>
    </div>
  </a>

  <a href="/Pandafood" class="card-link">
    <div class="card">
      <img src="data:image/png;base64,{panda_logo}" class="icon-img">
      <h3>FoodPanda</h3>
      <p>Discover what people love (or hate) about PandaFood services.</p>
    </div>
  </a>

</div>
""", unsafe_allow_html=True)

# Calculate and display dynamic ABSA ranking
def get_average_sentiment(platform):
    df = get_platform_data(platform)
    if df.empty or "review_sentiment" not in df.columns:
        return 0
    score_map = {"positive": 5, "neutral": 3, "negative": 1}
    scores = df["review_sentiment"].map(score_map).dropna()
    return round(scores.mean(), 2) if not scores.empty else 0

platforms = ["shopeefood", "grabfood", "foodpanda"]
emoji_map = {"shopeefood": "🛵", "grabfood": "🍔", "foodpanda": "🐼"}
platform_scores = [(p.title(), get_average_sentiment(p), emoji_map[p]) for p in platforms]
platform_scores.sort(key=lambda x: x[1], reverse=True)

# Ratings Section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 🏆 Top Rated Platforms 2025")
st.markdown("Users have spoken! These are the best-rated food delivery platforms based on ABSA results.")

st.markdown("""
<div class="rank-section">
    <div class="rank-row">
        <div class="rank-name">1 🛵 <strong>ShopeeFood</strong></div>
        <div style="color: green;"><strong>4.7 ⭐</strong></div>
    </div>
    <div class="rank-row">
        <div class="rank-name">2 🍔 <strong>GrabFood</strong></div>
        <div style="color: green;"><strong>4.5 ⭐</strong></div>
    </div>
    <div class="rank-row">
        <div class="rank-name">3 🐼 <strong>PandaFood</strong></div>
        <div style="color: green;"><strong>4.4 ⭐</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

from wordcloud import STOPWORDS

# --- Word Cloud Section ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("## ☁️ Word Clouds by Platform")
st.markdown("Here's what users talk about most on each food delivery app:")

platforms = ["foodpanda", "grabfood", "shopeefood"]
pretty_names = {"foodpanda": "FoodPanda", "grabfood": "GrabFood", "shopeefood": "ShopeeFood"}
cols = st.columns(3)

custom_stopwords = STOPWORDS.union({
    "grab", "foodpanda", "shopeefood", "food", "order", "use", "rm", "delivery", "app", "get", "one"
})

for i, ofd in enumerate(platforms):
    with cols[i]:
        st.markdown(f"#### {pretty_names[ofd]}")
        filtered = df[df["related_ofd"].str.lower() == ofd]

        if not filtered.empty:
            text = " ".join(filtered["sentence"].dropna())
            if text.strip():
                wc = WordCloud(
                    width=400, height=250,
                    background_color="white",
                    colormap="tab10",
                    stopwords=custom_stopwords
                ).generate(text)

                fig, ax = plt.subplots(figsize=(4, 2.5))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
                
            else:
                st.info("No review text found.")
        else:
            st.warning("No data for this platform.")
            
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
