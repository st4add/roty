import streamlit as st

def load_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .main-header {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #FF4B4B;
            text-align: center;
            padding: 2rem 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .category-header {
            color: #31333F;
            border-bottom: 2px solid #FF4B4B;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def show_celebration():
    st.balloons()
    st.toast('Vote Cast Successfully! 🎉', icon='✅')

def get_category_emoji(category):
    emojis = {
        "Ranelad of the Year": "👑",
        "Worst Ranelad of the Year": "🤡",
        "Most Improved Ranelad": "📈"
    }
    return emojis.get(category, "🗳️")

