import streamlit as st
import plotly.express as px
import pandas as pd
import time
import requests
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
    """Returns True if the user had a correct password."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    def password_entered():
        # Check if PASS exists in secrets first to prevent crash
        if "PASS" not in st.secrets:
            st.error("Developer Error: PASS not set in Streamlit Secrets.")
            return
            
        if st.session_state["password_input"] == st.secrets["PASS"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            st.error("😕 Password incorrect")

    st.text_input(
        "Enter the secret password to vote:", 
        type="password", 
        on_change=password_entered, 
        key="password_input"
    )
    return False

# Helper for live updates (st.fragment is preferred if available)
def live_update_wrapper(func):
    if hasattr(st, "fragment"):
        return st.fragment(run_every=1)(func)
    return func

@live_update_wrapper
def render_leaderboard(categories, key_prefix="default"):
    # Check if results are locked
    settings = dm.get_settings()
    is_locked = settings.get("results_locked", False)
    
    # Session state to track if current user has unlocked results for this session
    bypass_key = f"results_unlocked_{key_prefix}"
    if bypass_key not in st.session_state:
        st.session_state[bypass_key] = False
        
    if is_locked and not st.session_state[bypass_key]:
        st.warning("🔒 The live results are currently locked by the Admin.")
        
        with st.expander("Admin? Unlock to view"):
            unlock_pass = st.text_input("Enter DELPASS to view results", type="password", key=f"unlock_results_pass_{key_prefix}")
            if st.button("Unlock Results", key=f"unlock_results_btn_{key_prefix}", use_container_width=True):
                if "DELPASS" in st.secrets and unlock_pass == st.secrets["DELPASS"]:
                    st.session_state[bypass_key] = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
        return

    # Container for the live race
    race_container = st.container()
    
    with race_container:
        df = dm.get_results_df()
        
        for category in categories:
            # We call the function directly from the module
            try:
                html_str = utils.render_horse_race_html(category, df)
                if hasattr(st, "html"):
                    st.html(html_str)
                else:
                    st.markdown(html_str, unsafe_allow_html=True)
            except AttributeError:
                st.error("Wait... system is updating. Please refresh in 5 seconds.")
                st.stop()

    if st.button("Refresh & Sync Everything 🔄", key=f"refresh_btn_{key_prefix}", use_container_width=True):
        st.session_state.voted = False
        st.session_state.con_acknowledged = False
        st.rerun()

def get_voter_metadata():
    """Captures IP and Device info for auditing."""
    # 1. Get headers from Streamlit
    try:
        headers = st.context.headers
    except:
        headers = {}

    # 2. Robust IP extraction
    ip = "Unknown"
    for header in ["X-Forwarded-For", "x-forwarded-for", "X-Real-IP", "x-real-ip", "Remote-Addr"]:
        val = headers.get(header)
        if val and val != "Unknown":
            ip = val.split(",")[0].strip()
            break
    
    # 3. Handle local testing
    if ip == "Unknown" or ip.startswith("127.") or ip.startswith("192.168."):
        try:
            ip = requests.get('https://api.ipify.org', timeout=2).text
        except:
            pass

    # 4. Device Recognition
    ua = headers.get("User-Agent", headers.get("user-agent", "Unknown"))
    device = "Desktop/Other"
    if "iPhone" in ua: device = "iPhone"
    elif "Android" in ua: device = "Android Phone"
    elif "iPad" in ua: device = "iPad"
    elif "Macintosh" in ua: device = "Mac Desktop"
    elif "Windows" in ua: device = "Windows Desktop"
    
    return {
        "ip": ip, 
        "user_agent": device,
        "raw_ua": ua
    }

def main():
    utils.load_css()

    st.markdown("<h1 class='main-header'>🏆 ROTY Awards 🏆</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vote for the ultimate Ranelad of the Year!</p>", unsafe_allow_html=True)
    
    if not check_password():
        return

    # Get custom message from secrets
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

    tab1, tab2, tab3, tab4 = st.tabs(["🗳️ Vote", "📊 Leaderboard", "📋 Voter Log", "🛠️ Admin"])

    with tab1:
        with st.container(border=True):
            st.markdown("### 👤 Who are you?")
            # Use a scrollable container with radio buttons to prevent keyboard popup
            with st.container(height=250):
                voter_name = st.radio(
                    "Select your identity",
                    options=utils.RANELADS,
                    index=None,
                    label_visibility="collapsed",
                    key="voter_identity_radio"
                )

        if voter_name:
            # Check real-time database status
            has_voted_in_db = dm.has_voted(voter_name)

            if st.session_state.voted or has_voted_in_db:
                 if st.session_state.voted:
                     st.success("Thanks for voting! 🎉")
                 else:
                     st.info(f"Welcome back, {utils.decorate_name(voter_name)}! You have already cast your votes.")
                 
                 render_leaderboard(
                     categories=[
                        "Ranelad of the Year",
                        "Worst Ranelad of the Year",
                        "Most Improved Ranelad"
                     ], 
                     key_prefix="post_vote"
                 )
            else:
                # Handle Con's special acknowledgement locally in tab1
                if "Con" in voter_name and not st.session_state.con_acknowledged:
                    dialog_func = getattr(st, "dialog", getattr(st, "experimental_dialog", None))
                    if dialog_func:
                        @dialog_func("⚠️ Mandatory Acknowledgement")
                        def con_modal():
                            st.write("Before you can proceed, you must accept the truth.")
                            st.warning("Statistically, you are the worst Ranelad in history.")
                            st.markdown("""
                                <style>
                                div[role="dialog"] button, div[role="dialog"] [data-baseweb="button"] button {
                                    background-color: #000000 !important;
                                    border: 2px solid #FF4B4B !important;
                                }
                                div[role="dialog"] button *, div[role="dialog"] [data-baseweb="button"] button * {
                                    color: #FFFFFF !important;
                                    -webkit-text-fill-color: #FFFFFF !important;
                                    font-weight: 800 !important;
                                }
                                </style>
                            """, unsafe_allow_html=True)
                            if st.button(f"I, {voter_name}, acknowledge this fact 😔"):
                                st.session_state.con_acknowledged = True
                                st.rerun()
                        con_modal()
                        st.info("Please complete the acknowledgement popup to continue.")
                    else:
                        st.warning("⚠️ Statistically, you are the worst Ranelad in history.")
                        if st.button(f"I, {voter_name}, acknowledge this fact 😔"):
                            st.session_state.con_acknowledged = True
                            st.rerun()
                else:
                    # Show the actual voting form
                    with st.form("voting_form"):
                        st.markdown("### Cast Your Votes")
                        categories = ["Ranelad of the Year", "Worst Ranelad of the Year", "Most Improved Ranelad"]
                        votes_to_cast = {}
                        for category in categories:
                            with st.container(border=True):
                                st.markdown(f"**{utils.get_category_emoji(category)} {category}**")
                                # Filter out the voter's own name so they can't vote for themselves
                                candidate_options = [r for r in utils.RANELADS if r != voter_name]
                                
                                # Use a scrollable container with radio buttons to prevent keyboard popup
                                with st.container(height=200):
                                    candidate = st.radio(
                                        f"Nominee for {category}", 
                                        options=candidate_options,
                                        index=None,
                                        key=f"input_{category}",
                                        label_visibility="collapsed"
                                    )
                                if candidate:
                                    votes_to_cast[category] = candidate
                        if st.form_submit_button("Submit Votes 🚀", use_container_width=True):
                            if not votes_to_cast:
                                st.warning("Please vote for at least one category!")
                            else:
                                success = True
                                metadata = get_voter_metadata()
                                for cat, name in votes_to_cast.items():
                                    if not dm.save_vote(cat, name, voter_name, metadata=metadata):
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
            categories=["Ranelad of the Year", "Worst Ranelad of the Year", "Most Improved Ranelad"],
            key_prefix="main_tab"
        )

    with tab3:
        st.markdown("### 📋 Voter Turnout")
        voter_stats = dm.get_voter_stats()
        if voter_stats.empty:
            st.info("No voters yet.")
        else:
            # Apply decoration to voter names in the dataframe
            if "Voter" in voter_stats.columns:
                voter_stats["Voter"] = voter_stats["Voter"].apply(utils.decorate_name)
            st.dataframe(voter_stats, hide_index=True, use_container_width=True)

    with tab4:
        st.markdown("### 🛠️ Admin Zone")
        st.warning("Danger Zone!")
        
        # Section 1: Wipe Individual
        with st.container(border=True):
            st.markdown("#### 🗑️ Delete Individual Voter")
            voters = dm.list_voters()
            if not voters:
                st.info("No voters in the database yet.")
            else:
                # Create a mapping of decorated names to original names for deletion logic
                voter_options = {utils.decorate_name(v): v for v in voters}
                
                # Use scrollable radio for admin too for consistency and mobile friendliness
                with st.container(height=200):
                    selected_display = st.radio(
                        "Select voter to wipe", 
                        options=list(voter_options.keys()), 
                        index=None,
                        key="del_voter_radio"
                    )
                
                if selected_display:
                    voter_to_delete = voter_options[selected_display]
                    delpass = st.text_input("Enter DELPASS", type="password", key="del_pass")
                    if st.checkbox(f"Confirm wipe for {voter_to_delete}", key="del_conf"):
                        if st.button("Delete Permanently", type="primary", use_container_width=True):
                            if "DELPASS" not in st.secrets:
                                st.error("DELPASS not set in Secrets.")
                            elif delpass == st.secrets["DELPASS"]:
                                deleted = dm.delete_votes_for_voter(voter_to_delete)
                                st.toast(f"Wiped {deleted} votes!", icon="🗑️")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Wrong password")
        
        st.divider()
        
        # Section 2: Wipe All
        with st.container(border=True):
            st.markdown("#### 🧨 Reset ALL Data")
            if 'clear_clicks' not in st.session_state: st.session_state.clear_clicks = 0
            
            delpass_all = st.text_input("Enter DELPASS to authorize wipe", type="password", key="del_pass_all")
            
            if st.button("⚠️ WIPE EVERYTHING", use_container_width=True):
                if "DELPASS" not in st.secrets:
                    st.error("DELPASS not set in Secrets.")
                elif delpass_all != st.secrets["DELPASS"]:
                    st.error("Incorrect DELPASS")
                    st.session_state.clear_clicks = 0
                else:
                    st.session_state.clear_clicks += 1
                    if st.session_state.clear_clicks >= 10:
                        dm.clear_votes()
                        st.session_state.clear_clicks = 0
                        st.session_state.voted = False
                        st.toast("Wiped everything!", icon="🗑️")
                        time.sleep(1)
                        st.rerun()
                    else:
                        # Optional: provide no feedback on progress as requested "no indication"
                        pass

        st.divider()

        # Section 3: Results Visibility
        with st.container(border=True):
            st.markdown("#### 👁️ Results Visibility")
            settings = dm.get_settings()
            is_locked = settings.get("results_locked", False)
            
            st.info(f"Current Status: {'🔒 LOCKED' if is_locked else '🔓 PUBLIC'}")
            
            new_lock_state = st.checkbox("Lock Live Results", value=is_locked)
            
            if new_lock_state != is_locked:
                lock_pass = st.text_input("Enter DELPASS to change visibility", type="password", key="lock_pass")
                if st.button("Update Visibility", type="primary", use_container_width=True):
                    if "DELPASS" not in st.secrets:
                        st.error("DELPASS not set in Secrets.")
                    elif lock_pass == st.secrets["DELPASS"]:
                        dm.update_settings({"results_locked": new_lock_state})
                        st.toast(f"Results are now {'LOCKED' if new_lock_state else 'PUBLIC'}!", icon="👁️")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Wrong password")

    # --- Secret Sidebar Breakdown ---
    with st.sidebar:
        st.markdown("### 🕵️ God View")
        if "sidebar_authenticated" not in st.session_state:
            st.session_state.sidebar_authenticated = False
            
        if not st.session_state.sidebar_authenticated:
            side_pass = st.text_input("Enter Admin Password", type="password", key="sidebar_pass_input")
            if st.button("Unlock Breakdown", use_container_width=True):
                if "DELPASS" in st.secrets and side_pass == st.secrets["DELPASS"]:
                    st.session_state.sidebar_authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
        else:
            st.success("Access Granted")
            if st.button("Lock Sidebar", use_container_width=True):
                st.session_state.sidebar_authenticated = False
                st.rerun()
                
            st.markdown("#### 🗳️ Detailed Vote Log")
            votes = dm.load_votes()
            if not votes:
                st.info("No votes cast yet.")
            else:
                # Prepare data for display
                detailed_data = []
                for v in votes:
                    detailed_data.append({
                        "Voter": utils.decorate_name(v.get("voter", "Unknown")),
                        "Category": v.get("category", "Unknown"),
                        "Nominee": utils.decorate_name(v.get("candidate", "Unknown")),
                        "Time": pd.to_datetime(v.get("timestamp")).strftime('%H:%M:%S') if v.get("timestamp") else "Unknown"
                    })
                
                df_detailed = pd.DataFrame(detailed_data)
                # Show table without index for a cleaner look
                st.dataframe(df_detailed, hide_index=True, use_container_width=True)
                
                # Option to download as CSV for record keeping
                csv = df_detailed.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"roty_votes_detailed_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
