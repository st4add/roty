import streamlit as st
import plotly.express as px
import pandas as pd
import time
from data_manager import DataManager
import utils

# Page Configuration
st.set_page_config(
    page_title="ROTY Awards",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Data Manager
dm = DataManager()

def main():
    utils.load_css()

    st.markdown("<h1 class='main-header'>🏆 ROTY Awards 🏆</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vote for the ultimate Ranelad of the Year!</p>", unsafe_allow_html=True)
    
    # Initialize session state for post-vote redirect
    if 'voted' not in st.session_state:
        st.session_state.voted = False

    tab1, tab2 = st.tabs(["🗳️ Vote", "📊 Leaderboard"])

    with tab1:
        if st.session_state.voted:
             st.success("Thanks for voting! 🎉")
             if st.button("Vote Again?"):
                 st.session_state.voted = False
                 st.rerun()
             st.info("Check out the Leaderboard below!")
             
             render_leaderboard(
                 categories=[
                    "Ranelad of the Year",
                    "Worst Ranelad of the Year",
                    "Most Improved Ranelad"
                 ], 
                 key_prefix="post_vote"
             )
             
        else:
            st.markdown("### Cast Your Votes")
            
            categories = [
                "Ranelad of the Year",
                "Worst Ranelad of the Year",
                "Most Improved Ranelad"
            ]

            with st.form("voting_form"):
                # Voter Identification
                st.markdown("#### 👤 Identification")
                voter_name = st.selectbox(
                    "Who are you?",
                    options=["Select your name..."] + utils.RANELADS,
                    index=0,
                    help="Please identify yourself to vote."
                )

                st.markdown("---")
                
                votes_to_cast = {}
                
                for category in categories:
                    st.markdown(f"<h3 class='category-header'>{utils.get_category_emoji(category)} {category}</h3>", unsafe_allow_html=True)
                    
                    # Candidate Selection
                    candidate = st.selectbox(
                        f"Nominee for {category}", 
                        options=["Select a Ranelad..."] + utils.RANELADS,
                        index=0,
                        key=f"input_{category}",
                        help=f"Who deserves {category}?"
                    )
                    
                    if candidate and candidate != "Select a Ranelad...":
                        votes_to_cast[category] = candidate

                submitted = st.form_submit_button("Submit Votes 🚀")

                if submitted:
                    if voter_name == "Select your name...":
                        st.error("Please select your name first!")
                    elif not votes_to_cast:
                        st.warning("Please vote for at least one category!")
                    else:
                        success = True
                        for cat, name in votes_to_cast.items():
                            if not dm.save_vote(cat, name, voter_name):
                                success = False
                        
                        if success:
                            st.session_state.voted = True
                            utils.show_celebration()
                            time.sleep(1) # Let the user see the balloons
                            st.rerun()
                        else:
                            st.error("Something went wrong saving your votes.")

    with tab2:
        render_leaderboard(
            categories=[
                "Ranelad of the Year",
                "Worst Ranelad of the Year",
                "Most Improved Ranelad"
            ],
            key_prefix="main_tab"
        )

    # Sidebar footer
    with st.sidebar:
        st.markdown("---")
        st.markdown("Built for the Ranelads 🍻")

def render_leaderboard(categories, key_prefix="default"):
    st.markdown("### 📈 Live Results")
    
    # Refresh button
    if st.button("Refresh Data 🔄", key=f"refresh_btn_{key_prefix}"):
        st.rerun()

    df = dm.get_results_df()
    
    if df.empty:
        st.info("No votes cast yet. Be the first!")
    else:
        for category in categories:
            st.markdown(f"#### {utils.get_category_emoji(category)} {category}")
            
            cat_df = df[df['Category'] == category].copy()
            
            if cat_df.empty:
                st.text("No votes in this category yet.")
            else:
                # Sort descending for display (Top 1 first)
                cat_df = cat_df.sort_values(by="Count", ascending=False).reset_index(drop=True)
                
                # Display Top 3 in special styling
                for index, row in cat_df.iterrows():
                    rank = index + 1
                    name = row['Candidate']
                    count = row['Count']
                    
                    medal = ""
                    card_class = "leaderboard-card"
                    
                    if rank == 1:
                        medal = "🥇"
                        card_class += " rank-1"
                    elif rank == 2:
                        medal = "🥈"
                        card_class += " rank-2"
                    elif rank == 3:
                        medal = "🥉"
                        card_class += " rank-3"
                    else:
                        medal = f"#{rank}"
                    
                    st.markdown(f"""
                        <div class="{card_class}">
                            <span class="medal">{medal}</span>
                            <span class="candidate-name">{name}</span>
                            <span class="vote-count">{count}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.divider()

if __name__ == "__main__":
    main()
