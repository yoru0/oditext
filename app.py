import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title='Text Classification App',
    page_icon='📝',
    layout='centerd',
    initial_sidebar_state='expanded'
)


# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load('lr_model.joblib')
    except Exception as e:
        st.error(f'Error loading model: {e}')
        return None
    
model = load_model()


