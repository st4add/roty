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

    # Get custom message from secrets if it exists
    custom_insert = st.secrets.get("INSERT", "Also Simo is Gay")

    st.markdown(f"""
        <div style='background-color: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FF4B4B; margin-bottom: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <p style='font-size: 1.1rem; line-height: 1.6; color: #333;'>
                Welcome to the Ranelads of the Year Awards! 🎉 Tonight, we're celebrating the most iconic, extra, and utterly relatable moments of the year. 
                From meme-worthy fails to trend-setting wins, we're covering it all! 🍿 
                <br><br>
                Let's get this awards show started! 🎊 Who's ready for a night of laughs, nostalgia, and maybe a few surprise wins? 😏 
                <br><br>
                <strong>#RaneladsOfTheYear</strong> - <em>{custom_insert}</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'voted' not in st.session_state:
        st.session_state.voted = False
    if 'con_acknowledged' not in st.session_state:
        st.session_state.con_acknowledged = False

    tab1, tab2, tab3 = st.tabs(["🗳️ Vote", "📊 Leaderboard", "📋 Voter Log"])

    with tab1:
        # Identity Section (Always visible)
        with st.container(border=True):
            st.markdown("### 👤 Who are you?")
            voter_name = st.selectbox(
                "Select your identity",
                options=["Select your name..."] + utils.RANELADS,
                index=0,
                label_visibility="collapsed",
                key="voter_identity_select"
            )

        # Check real-time database status
        has_voted_in_db = False
        if voter_name != "Select your name...":
            has_voted_in_db = dm.has_voted(voter_name)

        # Show success view if they just voted OR already exist in DB
        if st.session_state.voted or has_voted_in_db:
             if st.session_state.voted:
                 st.success("Thanks for voting! 🎉")
             else:
                 st.info(f"Welcome back, {voter_name}! You have already cast your votes.")
             
             st.info("Check out the Leaderboard to see the results!")
             
             render_leaderboard(
                 categories=[
                    "Ranelad of the Year",
                    "Worst Ranelad of the Year",
                    "Most Improved Ranelad"
                 ], 
                 key_prefix="post_vote"
             )
             
        elif voter_name != "Select your name...":
            # Special acknowledgement for Con
            if voter_name == "Con" and not st.session_state.con_acknowledged:
                @st.experimental_dialog("⚠️ Mandatory Acknowledgement")
                def con_modal():
                    st.write("Before you can proceed, you must accept the truth.")
                    st.warning("Statistically, you are the worst Ranelad in history.")
                    
                    # Custom styling for the button inside the modal (robust selectors)
                    st.markdown("""
                        <style>
                        div[role="dialog"] button,
                        div[role="dialog"] [data-baseweb="button"] button {
                            background-color: #000000 !important;
                            border: 2px solid #FF4B4B !important;
                        }
                        div[role="dialog"] button,
                        div[role="dialog"] button * ,
                        div[role="dialog"] [data-baseweb="button"] button,
                        div[role="dialog"] [data-baseweb="button"] button * {
                            color: #FFFFFF !important;
                            -webkit-text-fill-color: #FFFFFF !important;
                            opacity: 1 !important;
                            font-weight: 800 !important;
                        }
                        div[role="dialog"] button:hover {
                            background-color: #333333 !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    if st.button("I, Con, acknowledge this fact 😔"):
                        st.session_state.con_acknowledged = True
                        st.rerun()

                con_modal()
                st.info("Please complete the acknowledgement popup to continue.")
                st.stop()

            # Show the voting form
            with st.form("voting_form"):
                st.markdown("### Cast Your Votes")
                
                categories = [
                    "Ranelad of the Year",
                    "Worst Ranelad of the Year",
                    "Most Improved Ranelad"
                ]
                
                votes_to_cast = {}
                
                for category in categories:
                    with st.container(border=True):
                        st.markdown(f"**{utils.get_category_emoji(category)} {category}**")
                        candidate = st.selectbox(
                            f"Nominee for {category}", 
                            options=["Select a Ranelad..."] + utils.RANELADS,
                            index=0,
                            key=f"input_{category}",
                            label_visibility="collapsed"
                        )
                        if candidate and candidate != "Select a Ranelad...":
                            votes_to_cast[category] = candidate

                submitted = st.form_submit_button("Submit Votes 🚀")

                if submitted:
                    if not votes_to_cast:
                        st.warning("Please vote for at least one category!")
                    else:
                        success = True
                        for cat, name in votes_to_cast.items():
                            if not dm.save_vote(cat, name, voter_name):
                                success = False
                        
                        if success:
                            st.session_state.voted = True
                            utils.show_celebration()
                            time.sleep(6)
                            st.rerun()
                        else:
                            st.error("Something went wrong saving your votes.")
        else:
            st.info("Please select your name above to start voting!")

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
            st.dataframe(
                voter_stats,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Voter": st.column_config.TextColumn("Ranelad"),
                    "Votes Cast": st.column_config.ProgressColumn(
                        "Participation", 
                        format="%d votes",
                        min_value=0, 
                        max_value=3
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

            voters = dm.list_voters()
            if not voters:
                st.info("No votes cast yet.")
            else:
                with st.popover("🗑️ Delete Individual Voter", use_container_width=True):
                    st.markdown("### Voter Deletion")
                    voter_to_delete = st.selectbox(
                        "Select voter to wipe",
                        options=["Select a voter..."] + voters,
                        index=0,
                        key="admin_voter_to_delete",
                    )

                    delpass = st.text_input(
                        "Enter DELPASS to confirm",
                        type="password",
                        key="admin_delpass",
                    )

                    confirm_delete = st.checkbox(
                        "Delete ALL votes for this person",
                        key="admin_confirm_delete_voter",
                    )

                    if st.button("Permanently Delete", key="admin_delete_voter_btn", type="primary", use_container_width=True):
                        if voter_to_delete == "Select a voter...":
                            st.error("Pick a voter.")
                        elif not confirm_delete:
                            st.error("Check the box.")
                        else:
                            try:
                                expected = st.secrets["DELPASS"]
                            except:
                                st.error("DELPASS not set in Secrets.")
                                st.stop()

                            if delpass != expected:
                                st.error("Wrong password.")
                            else:
                                deleted = dm.delete_votes_for_voter(voter_to_delete)
                                st.toast(f"Wiped {deleted} votes for {voter_to_delete}!", icon="🗑️")
                                time.sleep(1)
                                st.rerun()

            st.divider()
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
    
    if st.button("Refresh & Sync Everything 🔄", key=f"refresh_btn_{key_prefix}", use_container_width=True):
        st.session_state.voted = False
        st.session_state.con_acknowledged = False
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
                cat_df = cat_df.sort_values(by="Count", ascending=False).reset_index(drop=True)
                for index, row in cat_df.iterrows():
                    rank = index + 1
                    name = row['Candidate']
                    count = row['Count']
                    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                    card_class = "leaderboard-card"
                    if rank == 1: card_class += " rank-1"
                    elif rank == 2: card_class += " rank-2"
                    elif rank == 3: card_class += " rank-3"
                    
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
