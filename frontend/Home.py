#run >> python -m streamlit run Home.py
import streamlit as st
import base64
from model import get_platform_data


st.set_page_config(page_title="ABSA Food Dashboard", layout="wide", page_icon="🍽️")

st.markdown("<h1 style='text-align: center;'>🍽️ ABSA for Online Food Delivery Reviews</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Welcome to the Malaysian Sentiment Intelligence Dashboard</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

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
            background-color: #ffffff;
            border-radius: 15px;
            padding: 1.5rem;
            width: 260px;
            text-align: center;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            transition: 0.3s ease;
            cursor: pointer;
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

grab_logo = load_img_as_base64("images/grab.png")
shopee_logo = load_img_as_base64("images/shopee.png")
panda_logo = load_img_as_base64("images/panda.png")

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

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Built with 💙 by Russell Rangers</p>", unsafe_allow_html=True)
