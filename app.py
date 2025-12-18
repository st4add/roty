import streamlit as st
import plotly.express as px
import pandas as pd
from data_manager import DataManager
from auth import check_password, logout
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

    if not check_password():
        return

    # Tabs for different sections
    tab1, tab2 = st.tabs(["🗳️ Vote", "📊 Leaderboard"])

    with tab1:
        st.markdown("### Cast Your Votes")
        
        categories = [
            "Ranelad of the Year",
            "Worst Ranelad of the Year",
            "Most Improved Ranelad"
        ]

        # Use a form to group inputs
        with st.form("voting_form"):
            votes_to_cast = {}
            
            for category in categories:
                st.markdown(f"<h3 class='category-header'>{utils.get_category_emoji(category)} {category}</h3>", unsafe_allow_html=True)
                
                # Get existing candidates for autocomplete
                existing_candidates = dm.get_candidates(category)
                
                # Using selectbox with custom input enabled (simulated via text_input if not found)
                # Streamlit's selectbox doesn't support direct custom entry easily combined with search,
                # so we'll use a text input with an optional selectbox helper or just a clean text input with autocomplete suggestions if possible.
                # Actually, st.selectbox doesn't do 'allow_new' out of the box nicely without a workaround.
                # Let's use a clear text input for simplicity and flexibility as requested ("input the names after").
                # To make it user friendly, we can show a list of top candidates or recent ones, but plain text is safest for "open entry".
                
                # Enhanced: Multiselect-like behavior or just text? 
                # Request said "input the names after". Let's do a text input.
                
                candidate = st.text_input(
                    f"Nominee for {category}", 
                    key=f"input_{category}",
                    placeholder="Enter name here...",
                    help=f"Who deserves {category}?"
                )
                if candidate:
                    votes_to_cast[category] = candidate.strip()

            submitted = st.form_submit_button("Submit Votes 🚀")

            if submitted:
                if not votes_to_cast:
                    st.warning("Please enter at least one name to vote!")
                else:
                    success = True
                    for cat, name in votes_to_cast.items():
                        if not dm.save_vote(cat, name):
                            success = False
                    
                    if success:
                        utils.show_celebration()
                        # Optional: clear cache or state if needed, but form clears on rerun usually if not persistent
                    else:
                        st.error("Something went wrong saving your votes.")

    with tab2:
        st.markdown("### 📈 Live Results")
        
        # Refresh button
        if st.button("Refresh Data 🔄"):
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
                    cat_df = cat_df.sort_values(by="Count", ascending=True) # Sort for bar chart (bottom to top)
                    
                    fig = px.bar(
                        cat_df,
                        x="Count",
                        y="Candidate",
                        orientation='h',
                        text="Count",
                        color="Count",
                        color_continuous_scale="Reds"
                    )
                    
                    fig.update_layout(
                        showlegend=False,
                        xaxis_title=None,
                        yaxis_title=None,
                        height=300,
                        margin=dict(l=0, r=0, t=0, b=0),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()

    # Sidebar footer
    with st.sidebar:
        st.markdown("---")
        if st.button("Log Out"):
            logout()
        st.markdown("Built for the Ranelads 🍻")

if __name__ == "__main__":
    main()

