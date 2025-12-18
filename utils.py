import streamlit as st

RANELADS = [
    "David", "Enda", "Rob", "Jack", "Monz", "Ois", "Ollie", "Con", 
    "Kill", "Pauly", "Simo", "Petch", "Vinny", "Lorcan", "Thilo", 
    "Carl", "Cramps", "Gibb", "Hugo", "Boydie", "Josh", "Jam"
]

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
        
        /* Modern Leaderboard Styles */
        .leaderboard-card {
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            border: 1px solid rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .leaderboard-card:hover {
            transform: translateY(-2px);
        }
        .rank-1 {
            background: linear-gradient(to right, #fff, #fff9c4);
            border: 2px solid #ffd700;
        }
        .rank-2 {
            background: linear-gradient(to right, #fff, #f5f5f5);
            border: 2px solid #c0c0c0;
        }
        .rank-3 {
            background: linear-gradient(to right, #fff, #fff0e6);
            border: 2px solid #cd7f32;
        }
        .medal {
            font-size: 2rem;
            margin-right: 1rem;
        }
        .candidate-name {
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
        }
        .vote-count {
            font-size: 1.5rem;
            font-weight: 800;
            color: #FF4B4B;
            float: right;
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
