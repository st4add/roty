import streamlit as st

# Updated to trigger refresh on Streamlit Cloud
RANELADS = sorted([
    "David 👑", "Enda", "Rob 👑", "Jack 👑", "Pauly", "Simo 👑", "Petch", "Vinny", 
    "Lorcan", "Thilo", "Carl", "Cramps", "Gibb", "Hugo", "Boydie", 
    "Josh", "Jam", "Monz", "Ois", "Ollie", "Con 💩💩", "Kill 👑"
])

def load_css():
    """Loads custom CSS with no leading indentation to avoid markdown code blocks."""
    css = """<style>
.stApp { background: #f0f2f6; overflow-x: hidden; }
h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
.main-header { color: #FF4B4B; text-align: center; padding: 1rem 0 2rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.05); font-size: 2.5rem; }

/* General Container Styling */
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

/* Tab Styling */
div[data-testid="stTabs"] button { font-size: 1rem; padding: 0.5rem 1rem; }
@media (max-width: 640px) {
    div[data-testid="stTabs"] button { font-size: 0.8rem; padding: 0.4rem 0.6rem; }
    div[data-testid="stTabs"] button p { font-size: 0.9rem; }
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* Mobile Tweaks */
@media (max-width: 640px) {
    .main-header { font-size: 2rem; padding: 1rem 0; }
    .stButton>button { padding: 1rem; }
    .main .block-container { padding-bottom: 10rem !important; }
}

/* Horse Race Styling */
.race-track-container { background: #2e7d32; padding: 1.5rem 1rem; border-radius: 12px; margin-bottom: 2rem; position: relative; border: 4px solid #1b5e20; box-shadow: inset 0 0 20px rgba(0,0,0,0.3); overflow: hidden; }
.race-track-header { color: white; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem; text-align: center; font-size: 1.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
.horse-lane { height: 60px; border-bottom: 1px dashed rgba(255,255,255,0.2); position: relative; display: flex; align-items: center; }
.horse-lane:last-child { border-bottom: none; }
@keyframes jitter {
    0% { transform: translate(0, 0); }
    25% { transform: translate(2px, 1px); }
    50% { transform: translate(-1px, -1px); }
    75% { transform: translate(1px, -2px); }
    100% { transform: translate(0, 0); }
}
.horse-container { position: absolute; transition: left 1s linear; display: flex; align-items: center; animation: jitter 0.2s infinite ease-in-out; white-space: nowrap; }
.horse-emoji { font-size: 2.5rem; margin-right: 8px; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.3)); transform: scaleX(-1); display: inline-block; }
.horse-name { color: white; font-weight: 800; font-size: 0.9rem; text-shadow: 1px 1px 2px black; background: rgba(0,0,0,0.4); padding: 2px 8px; border-radius: 4px; }
.finish-line { position: absolute; right: 40px; top: 0; bottom: 0; width: 10px; background: repeating-linear-gradient(0deg, #fff, #fff 10px, #000 10px, #000 20px); box-shadow: 2px 0 5px rgba(0,0,0,0.3); z-index: 1; }

/* Simplified Name Selection Buttons */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 8px !important;
    padding: 2px !important;
}
div[data-testid="stRadio"] label {
    background: #f8f9fb !important;
    padding: 12px 16px !important;
    border-radius: 12px !important;
    border: 1px solid #e0e0e0 !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    display: flex !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
div[data-testid="stRadio"] label:hover {
    background: #f0f2f6 !important;
    border-color: #cccccc !important;
}
/* Hide the default radio circle */
div[data-testid="stRadio"] input[type="radio"] { display: none !important; }
/* Selected state */
div[data-testid="stRadio"] label:has(input:checked) {
    background: #FF4B4B !important;
    border-color: #FF4B4B !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3) !important;
}
div[data-testid="stRadio"] label:has(input:checked) p {
    color: white !important;
    font-weight: 700 !important;
}
div[data-testid="stRadio"] label p {
    font-size: 1.1rem !important;
    margin: 0 !important;
    padding: 0 !important;
}
/* Remove side padding from scroll containers */
div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {
    padding-left: 4px !important;
    padding-right: 4px !important;
}
</style>"""
    st.markdown(css, unsafe_allow_html=True)

def show_celebration():
    # Custom cascading text effect
    st.markdown("""<style>
@keyframes fall {
    0% { top: -10%; opacity: 1; transform: rotate(0deg); }
    100% { top: 110%; opacity: 0; transform: rotate(360deg); }
}
.rain-drop {
    position: fixed;
    top: -10%;
    z-index: 999999;
    pointer-events: none;
    font-weight: bold;
    font-family: 'Helvetica Neue', sans-serif;
    animation: fall 8s linear forwards;
}
</style>""", unsafe_allow_html=True)
    
    rain_html = ""
    import random
    colors = ['#FF4B4B', '#FFD700', '#4CAF50', '#2196F3', '#9C27B0']
    
    for i in range(50):
        left = random.randint(0, 100)
        duration = random.uniform(5, 10)
        delay = random.uniform(0, 3)
        size = random.randint(20, 50)
        color = random.choice(colors)
        
        rain_html += f'<div class="rain-drop" style="left: {left}vw; animation-duration: {duration}s; animation-delay: {delay}s; font-size: {size}px; color: {color};">Simo 🌈</div>'
        
    st.markdown(rain_html, unsafe_allow_html=True)

def decorate_name(name):
    """Adds crowns or other emojis to specific names for display."""
    if not name:
        return name
    
    clean_name = name.replace(" 👑", "").replace(" 💩💩", "").strip()
    
    if clean_name == "Con":
        return f"{clean_name} 💩💩"
    
    vips = ["David", "Rob", "Kill", "Jack", "Simo"]
    if clean_name in vips:
        return f"{clean_name} 👑"
    return name

def render_horse_race_html(category, results_df):
    """Generates the HTML for a single category horse race with NO leading indentation."""
    # Create a map of existing votes
    votes_map = {row['Candidate']: row['Count'] for _, row in results_df[results_df['Category'] == category].iterrows()}
    
    # We want ALL horses to appear on the track
    # Header - NO INDENTATION to avoid triggering markdown code blocks
    html = f'<div class="race-track-container"><div class="race-track-header">{category}</div><div class="finish-line"></div>'
    
    # Track only Ranelads who have at least one vote to avoid overcrowding the screen
    voted_horses = []
    for r in RANELADS:
        count = votes_map.get(r, 0)
        if count > 0:
            voted_horses.append({'name': r, 'count': count})
    
    if not voted_horses:
        html += '<div style="color: white; text-align: center; padding: 2rem;">The horses are still in the gate... (No votes yet)</div>'
    else:
        # Sort by count descending
        voted_horses = sorted(voted_horses, key=lambda x: x['count'], reverse=True)
        
        # Finish line is 15 votes
        finish_line_votes = 15
        
        for horse in voted_horses:
            name = decorate_name(horse['name'])
            count = horse['count']
            
            # Progress: absolute based on vote count
            progress = min((count / finish_line_votes) * 85, 85)
            
            html += f'<div class="horse-lane"><div class="horse-container" style="left: {progress}%;"><span class="horse-emoji">🐎</span><span class="horse-name">{name} ({count} votes)</span></div></div>'
            
    html += '</div>'
    return html

def get_category_emoji(category):
    emojis = {
        "Ranelad of the Year": "👑",
        "Worst Ranelad of the Year": "🤡",
        "Most Improved Ranelad": "📈"
    }
    return emojis.get(category, "🗳️")
