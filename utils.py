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
            background: #f0f2f6;
        }
        
        /* Typography */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
        }
        
        .main-header {
            color: #FF4B4B;
            text-align: center;
            padding: 1rem 0 2rem 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
            font-size: 2.5rem;
        }
        
        /* Style Streamlit Native Containers to look like cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white;
            border-radius: 16px;
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 16px;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 0.75rem 1rem;
            background: #FF4B4B;
            color: white;
            border: none;
            box-shadow: 0 4px 6px rgba(255, 75, 75, 0.2);
            transition: all 0.2s ease;
            margin-top: 1rem;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(255, 75, 75, 0.3);
            background: #ff3333;
            color: white;
        }
        
        /* Leaderboard Styling */
        .leaderboard-card {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
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
            font-size: 1.8rem;
            min-width: 40px;
        }
        .candidate-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #374151;
            flex-grow: 1;
            padding: 0 1rem;
        }
        .vote-count {
            font-size: 1.2rem;
            font-weight: 800;
            color: #FF4B4B;
            background: #fff1f1;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
        }
        
        /* Hide default elements */
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        
        /* Mobile Tweaks */
        @media (max-width: 640px) {
            .main-header {
                font-size: 2rem;
                padding: 1rem 0;
            }
            .stButton>button {
                padding: 1rem;
            }
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
