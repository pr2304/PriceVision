import streamlit as st
from streamlit_lottie import st_lottie
import requests

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="PriceVision | Real Estate Predictor",
    page_icon="🏙",
    layout="wide"
)

# ------------------ HELPER: LOAD ANIMATION ------------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json")

# ------------------ CUSTOM CSS (PURE DARK THEME) ------------------
st.markdown("""
    <style>
        /* Background and global text */
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
        }
        [data-testid="stSidebar"] {
            background-color: #11141c !important;
        }
        h1, h2, h3, h4, h5, h6, p, li, div {
            color: #f5f5f5 !important;
        }

        /* Headings */
        .main-title {
            font-size: 2.6rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sub-title {
            font-size: 1.2rem;
            color: #d1d5db;
        }

        /* Card container (dark mode cards) */
        .feature-card {
            background: linear-gradient(145deg, #1b1f2a, #161922);
            border-radius: 18px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            transition: all 0.3s ease-in-out;
            height: 270px;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(0, 180, 255, 0.3);
        }
        .feature-title {
            color: #38bdf8;
            font-weight: 700;
            font-size: 1.3rem;
        }
        .feature-desc {
            color: #cbd5e1;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(90deg, #2563eb, #0ea5e9);
            color: white;
            border: none;
            padding: 0.6rem 1rem;
            border-radius: 10px;
            font-weight: 600;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            transform: scale(1.05);
        }

        /* Divider */
        hr {
            border: 1px solid #1e293b;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<h1 class='main-title'>🏙 PriceVision</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Your Smart Real Estate Price Prediction Assistant</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ HERO SECTION ------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    if animation:
        st_lottie(animation, height=350, key="home_anim")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/619/619034.png", use_container_width=True)

with col2:
    st.markdown("#### 💡 Welcome to PriceVision!")
    st.markdown(
        """
        <div style='background-color:#161922; padding:1.5rem; border-radius:15px;'>
        Harness the power of <b>AI</b> to make smarter real estate decisions.  
        <br><br>
        <b>PriceVision</b> helps you:
       <ul>
       <li>💰 Predict property prices instantly using smart machine learning model</li>
       <li>🗺️ Visualize housing trends across sectors with interactive GeoMaps</li>
       <li>🏢 Get smart apartment recommendations tailored to your needs</li>
       </ul>

        Whether you’re a buyer, seller, or investor — <b>PriceVision</b> empowers you with data-driven insights.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ DASHBOARD CARDS ------------------
st.subheader("✨ Explore PriceVision Features")

col1, col2, col3 = st.columns(3, gap="large")

# Helper function for dark cards
def feature_card(title, description, button_label, page_name, icon_url):
    st.markdown(
        f"""
        <div class="feature-card">
            <div style="text-align:center;">
                <img src="{icon_url}" width="60" style="filter: invert(1); opacity: 0.9;">
            </div>
            <h3 class="feature-title" style="text-align:center;">{title}</h3>
            <p class="feature-desc" style="text-align:center;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='text-align:center; margin-top:-1rem;'>", unsafe_allow_html=True)
    if st.button(button_label, use_container_width=True):
        st.switch_page(page_name)
    st.markdown("</div>", unsafe_allow_html=True)


with col1:
    feature_card("Price Predictor",
                 "Estimate property prices instantly using our AI-powered model.",
                 "Open Predictor",
                 "pages/1_Price Predictor.py",
                 "https://cdn-icons-png.flaticon.com/512/10668/10668083.png")

with col2:
    feature_card("Housing Insights",
                 "Explore housing trends, price patterns, and sector-based insights.",
                 "Open Insights",
                 "pages/2_Housing Insights.py",
                 "https://cdn-icons-png.flaticon.com/512/7763/7763773.png")

with col3:
    feature_card("Apartment Recommender",
                 "Get personalized apartment suggestions based on your preferences.",
                 "Open Recommender",
                 "pages/3_Apartment Recommender.py",
                 "https://cdn-icons-png.flaticon.com/512/6917/6917662.png")

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown(
    "<p style='text-align:center; color:#9ca3af;'>Made with ❤️ by <b>Team PriceVision</b></p>",
    unsafe_allow_html=True
)
