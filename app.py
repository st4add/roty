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

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["PASS"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password in session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Enter the secret password to vote:", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Enter the secret password to vote:", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

def main():
    utils.load_css()

    st.markdown("<h1 class='main-header'>🏆 ROTY Awards 🏆</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vote for the ultimate Ranelad of the Year!</p>", unsafe_allow_html=True)
    
    if not check_password():
        return

    st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FF4B4B; margin-bottom: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <p style='font-size: 1.1rem; line-height: 1.6; color: #333;'>
                Welcome to the Ranelads of the Year Awards! 🎉 Tonight, we're celebrating the most iconic, extra, and utterly relatable moments of the year. 
                From meme-worthy fails to trend-setting wins, we're covering it all! 🍿 
                <br><br>
                Let's get this awards show started! 🎊 Who's ready for a night of laughs, nostalgia, and maybe a few surprise wins? 😏 
                <br><br>
                <strong>#RaneladsOfTheYear</strong> - <em>Also Simo is Gay</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for post-vote redirect
    if 'voted' not in st.session_state:
        st.session_state.voted = False

    tab1, tab2, tab3 = st.tabs(["🗳️ Vote", "📊 Leaderboard", "📋 Voter Log"])

    with tab1:
        if st.session_state.voted:
             st.success("Thanks for voting! 🎉")
             st.info("Check out the Leaderboard to see the results!")
             
             render_leaderboard(
                 categories=[
                    "Ranelad of the Year",
                    "Worst Ranelad of the Year",
                    "Most Improved Ranelad"
                 ], 
                 key_prefix="post_vote"
             )
             
        else:
            # Identity Section
            with st.container(border=True):
                st.markdown("### 👤 Who are you?")
                voter_name = st.selectbox(
                    "Select your identity",
                    options=["Select your name..."] + utils.RANELADS,
                    index=0,
                    label_visibility="collapsed"
                )

            # Check if this user has already voted
            has_already_voted = False
            if voter_name != "Select your name...":
                if dm.has_voted(voter_name):
                    has_already_voted = True
                    st.error(f"⚠️ Sorry {voter_name}, you have already voted! One vote per Ranelad.")
                    st.info("Check the 'Voter Log' tab if you think this is a mistake.")

            if not has_already_voted:
                with st.form("voting_form"):
                    
                    categories = [
                        "Ranelad of the Year",
                        "Worst Ranelad of the Year",
                        "Most Improved Ranelad"
                    ]
                    
                    votes_to_cast = {}
                    
                    for category in categories:
                        with st.container(border=True):
                            # Header
                            st.markdown(f"**{utils.get_category_emoji(category)} {category}**")
                            
                            # Candidate Selection
                            candidate = st.selectbox(
                                f"Nominee for {category}", 
                                options=["Select a Ranelad..."] + utils.RANELADS,
                                index=0,
                                key=f"input_{category}",
                                help=f"Who deserves {category}?",
                                label_visibility="collapsed"
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
                                time.sleep(6) # Increased wait time to let animation finish!
                                st.rerun()
                            else:
                                st.error("Something went wrong saving your votes.")
            else:
                # If they have voted, maybe show a "View Results" button instead of the form
                if st.button("View Results 📊"):
                    # We can't switch tabs easily, but we can show the leaderboard here
                    st.session_state.voted = True
                    st.rerun()

    with tab2:
        render_leaderboard(
            categories=[
                "Ranelad of the Year",
                "Worst Ranelad of the Year",
                "Most Improved Ranelad"
            ],
            key_prefix="main_tab"
        )

    with tab3:
        st.markdown("### 📋 Voter Turnout")
        st.markdown("Check who has exercised their democratic right!")
        
        if st.button("Refresh Log 🔄", key="refresh_log"):
            st.rerun()
            
        voter_stats = dm.get_voter_stats()
        
        if voter_stats.empty:
            st.info("No voters yet.")
        else:
            # Display as a nice interactive dataframe or table
            st.dataframe(
                voter_stats,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Voter": st.column_config.TextColumn("Ranelad", help="The voter"),
                    "Votes Cast": st.column_config.ProgressColumn(
                        "Participation", 
                        format="%d votes",
                        min_value=0, 
                        max_value=3,
                        help="Number of categories voted for"
                    ),
                    "Last Voted": "Timestamp"
                }
            )

    # Sidebar footer
    with st.sidebar:
        st.markdown("---")
        st.markdown("Built for the Ranelads 🍻")
        
        # Admin Zone
        with st.expander("Admin Zone", expanded=False):
            st.warning("Danger Zone!")
            if 'clear_clicks' not in st.session_state:
                st.session_state.clear_clicks = 0
                
            if st.button("⚠️ Reset All Votes", key="reset_btn"):
                st.session_state.clear_clicks += 1
                clicks_needed = 10 - st.session_state.clear_clicks
                
                if clicks_needed <= 0:
                    dm.clear_votes()
                    st.session_state.clear_clicks = 0
                    st.session_state.voted = False
                    st.toast("All votes have been cleared!", icon="🗑️")
                    time.sleep(1)
                    st.rerun()

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
