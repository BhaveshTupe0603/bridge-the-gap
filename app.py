import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bridge-The-Gap", page_icon="🎓", layout="centered")

# --- API KEY SETUP ---
# It will look in st.secrets first. 
# If not there, it checks the variable. 
# If still not there, it shows a sidebar input.
api_key_from_secrets = st.secrets.get("GOOGLE_API_KEY")

# TESTING ONLY: Paste your key here if you aren't using secrets.toml yet:
# api_key_from_secrets = "AIzaSy..." 

if api_key_from_secrets:
    GOOGLE_API_KEY = api_key_from_secrets
else:
    st.sidebar.warning("API Key not found in Secrets.")
    GOOGLE_API_KEY = st.sidebar.text_input("Enter Google API Key:", type="password")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # Using the specific 2.5-flash model from your available list
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Configuration Error: {e}")
        st.stop()
else:
    st.info("👋 Please enter your Google API Key to begin.")
    st.stop()

# --- UI DESIGN ---
st.title("🌉 Bridge-The-Gap")
st.subheader("Find Your Missing Knowledge")
st.markdown("""
    Struggling with a complex topic? Paste it below, and we'll identify the 
    **3 fundamental concepts** you need to master first.
""")

# Text Input
target_topic = st.text_input("What topic is confusing you?", placeholder="e.g., Eigenvalues, Backpropagation, CRISPR")

# Analyze Button
if st.button("Analyze Prerequisites"):
    if target_topic:
        with st.spinner(f"Using Gemini 2.5 to analyze '{target_topic}'..."):
            # Refined Prompt for Gemini 2.5
            prompt = f"""
            Identify the top 3 most important prerequisite concepts needed BEFORE learning "{target_topic}".
            
            For each concept, provide:
            1. The Concept Name (as a heading).
            2. A simple, 1-sentence definition for a beginner.
            
            Format the response clearly using Markdown.
            """
            
            try:
                # API Call
                response = model.generate_content(prompt)
                
                # Display Results
                st.divider()
                st.success(f"To understand **{target_topic}**, master these first:")
                st.markdown(response.text)
                
                st.info("💡 **Hackathon Tip:** Master these foundations first to make the complex topic easy!")
                
            except Exception as e:
                # If 2.5-flash is still acting up, this will tell us exactly why
                st.error(f"An error occurred: {e}")
                st.info("Note: Ensure your API Key has 'Generative AI Training' or 'Pay-as-you-go' enabled if required for 2.5 models.")
    else:
        st.warning("Please enter a topic first!")

# --- FOOTER ---
st.markdown("---")
st.caption("Bridge-The-Gap Prototype | Powered by Gemini 2.5 Flash")