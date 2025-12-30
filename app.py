import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bridge-The-Gap", page_icon="🎓")

# --- API KEY SETUP ---
# Priority: 1. Streamlit Secrets, 2. Manual Variable, 3. User Input
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") 

# TESTING PURPOSES: If you want to hardcode for a quick test, paste it here:
# GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

if not GOOGLE_API_KEY:
    st.sidebar.warning("API Key not found in secrets.")
    GOOGLE_API_KEY = st.sidebar.text_input("Enter Google API Key:", type="password")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Please provide a Google API Key to continue.")
    st.stop()

# --- UI DESIGN ---
st.title("🌉 Bridge-The-Gap")
st.subheader("Find Your Missing Knowledge")
st.markdown("""
    Struggling with a complex topic? Paste it below, and we'll identify the 
    **3 fundamental concepts** you need to master first to understand it.
""")

# Input section
target_topic = st.text_input("What topic is confusing you?", placeholder="e.g. Eigenvalues, Quantum Entanglement, Backpropagation")

analyze_button = st.button("Analyze Prerequisites")

# --- LOGIC ---
if analyze_button:
    if target_topic:
        with st.spinner(f"Analyzing the foundations of {target_topic}..."):
            # The Prompt
            prompt = f"""
            You are an expert tutor helping a student who is stuck. 
            The student wants to learn about: "{target_topic}".
            
            Identify the top 3 most important prerequisite concepts they need to understand BEFORE learning "{target_topic}".
            For each prerequisite:
            1. Provide the name of the concept.
            2. Provide a simple, 1-sentence definition.
            
            Format the output exactly like this:
            ### 1. [Concept Name]
            [1-sentence definition]
            
            ### 2. [Concept Name]
            [1-sentence definition]
            
            ### 3. [Concept Name]
            [1-sentence definition]
            """

            try:
                response = model.generate_content(prompt)
                
                # UI Display of results
                st.divider()
                st.success(f"To understand **{target_topic}**, you should first master these:")
                st.markdown(response.text)
                
                st.info("💡 **Tip:** Master these in order, and the main topic will become much clearer!")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a topic first!")

# --- FOOTER ---
st.markdown("---")
st.caption("Built for Hackathon Prototype: Bridge-The-Gap")