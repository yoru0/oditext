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


# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []


# Function to classify text
def classify_text(text):
    if model is not None:
        try:
            prediction = model.predict([text])[0]
            prediction_proba = model.predict_proba([text])[0]
            confidence = max(prediction_proba) * 100
            
            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.history.append({
                "timestamp": timestamp,
                "text": text,
                "prediction": prediction,
                "confidence": confidence
            })
            
            return prediction, confidence
        except Exception as e:
            st.error(f"Error during classification: {e}")
            return None, None
    return None, None


# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Text Classification", "History"])


# Main content based on selected page
if page == "Text Classification":
    st.title("Text Classification")
    st.write("Enter text below to classify it using the pre-trained model.")
    
    # Input text
    text_input = st.text_area("Enter text to classify:", height=150)
    
    # Classify button
    if st.button("Classify"):
        if text_input.strip() != "":
            with st.spinner("Classifying..."):
                prediction, confidence = classify_text(text_input)
                
                if prediction is not None:
                    st.success(f"Classification complete!")
                    
                    # Display result in a nice format
                    st.subheader("Result:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Prediction", prediction)
                    with col2:
                        st.metric("Confidence", f"{confidence:.2f}%")
        else:
            st.warning("Please enter some text to classify.")
    
    # Information about the model
    with st.expander("About the Model"):
        st.write("""
        This application uses a pre-trained model to classify text.
        The model is loaded from 'lr_model.joblib'.
        """)

elif page == "History":
    st.title("Classification History")
    
    if st.session_state.history:
        # Convert history to DataFrame for better display
        history_df = pd.DataFrame(st.session_state.history)
        
        # Add a button to clear history
        if st.button("Clear History"):
            st.session_state.history = []
            st.experimental_rerun()
        
        # Display history table
        st.dataframe(
            history_df,
            column_config={
                "timestamp": "Time",
                "text": "Input Text",
                "prediction": "Classification",
                "confidence": st.column_config.NumberColumn(
                    "Confidence",
                    format="%.2f%%"
                )
            },
            hide_index=True
        )
    else:
        st.info("No classification history available. Classify some text first!")
