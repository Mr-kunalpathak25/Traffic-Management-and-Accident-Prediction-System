import streamlit as st

def show_hierarchies():
    st.subheader("📊 Concept Hierarchies")

    st.markdown("""
    ### Time Hierarchy
    - **Day** → **Month** → **Quarter** → **Year**
    
    ### Location Hierarchy
    - **City** → **State** → **Country**
    
    ### Weather Condition Hierarchy
    - **Temperature (°C)** → **Weather Category (Hot, Mild, Cold)**
    
    ### Traffic Volume
    - **Vehicle Count** → **Traffic Density (Low, Medium, High)**
    """)
