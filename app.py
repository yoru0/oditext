import streamlit as st
import pickle
import joblib
import pandas as pd
from datetime import datetime
import os, re

# Page configuration
st.set_page_config(
    page_title="Mental Health Text Classification",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------
custom_stopwords = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
    "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
    "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
    "weren't", 'won', "won't", 'wouldn', "wouldn't"
]

def custom_tokenizer(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]+", "", text)
    tokens = text.split()
    return [t for t in tokens if t not in custom_stopwords]

# Load the model
@st.cache_resource
def load_model():
    try:
        with open('lr2.pkl', 'rb') as f:
            return pickle.load(f)
        # return joblib.load('lr.joblib')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Initialize or load history from CSV
def init_history():
    if os.path.exists('history.csv'):
        try:
            return pd.read_csv('history.csv')
        except Exception as e:
            st.warning(f"Error loading history file: {e}. Starting with empty history.")
            return pd.DataFrame(columns=["timestamp", "text", "prediction", "confidence_score"])
    else:
        return pd.DataFrame(columns=["timestamp", "text", "prediction", "confidence_score"])

# Save history to CSV
def save_history(history_df):
    try:
        history_df.to_csv('history.csv', index=False)
    except Exception as e:
        st.error(f"Error saving history: {e}")

# Initialize history
if 'history_df' not in st.session_state:
    st.session_state.history_df = init_history()

# Function to classify text
def classify_text(text):
    if model is not None and text.strip() != "":
        try:
            prediction_proba = model.predict_proba([text])[0]
            
            normal_percentage = prediction_proba[0] * 100
            depressed_percentage = prediction_proba[1] * 100
            
            # Determine prediction class
            if depressed_percentage > normal_percentage:
                prediction = "Depressed"
                confidence = depressed_percentage
            else:
                prediction = "Normal"
                confidence = normal_percentage
            
            # Add to history DataFrame
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = pd.DataFrame([{
                "timestamp": timestamp,
                "text": text,
                "prediction": prediction,
                "confidence_score": confidence
            }])
            
            st.session_state.history_df = pd.concat([st.session_state.history_df, new_entry], ignore_index=True)
            
            # Save updated history
            save_history(st.session_state.history_df)
            
            return prediction, confidence, depressed_percentage, normal_percentage
            
        except Exception as e:
            st.error(f"Error during classification: {e}")
            return None, None, None, None
    return None, None, None, None

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
                prediction, confidence, depressed_pct, suicide_pct = classify_text(text_input)
                
                if prediction is not None:
                    st.success(f"Classification complete!")
                    
                    # Display result in a nice format
                    st.subheader("Result:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Prediction", prediction)
                    with col2:
                        st.metric("Confidence", f"{confidence:.2f}%")
                    
                    # Show probability breakdown
                    st.subheader("Probability Breakdown:")
                    breakdown_cols = st.columns(2)
                    with breakdown_cols[0]:
                        st.metric("Depressed", f"{depressed_pct:.2f}%")
                    with breakdown_cols[1]:
                        st.metric("Suicidal", f"{suicide_pct:.2f}%")
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
    
    if not st.session_state.history_df.empty:
        # Display history table
        st.dataframe(
            st.session_state.history_df,
            column_config={
                "timestamp": "Time",
                "text": "Text Input",
                "prediction": "Classification",
                "confidence_score": st.column_config.NumberColumn(
                    "Confidence",
                    format="%.2f%%"
                )
            },
            hide_index=True
        )
        
        # Add a button to clear history
        if st.button("Clear History"):
            st.session_state.history_df = pd.DataFrame(columns=["timestamp", "text", "prediction", "confidence_score"])
            save_history(st.session_state.history_df)
            st.experimental_rerun()
            
        # Download history as CSV
        csv = st.session_state.history_df.to_csv(index=False)
        st.download_button(
            label="Download History CSV",
            data=csv,
            file_name="classification_history.csv",
            mime="text/csv",
        )
    else:
        st.info("No classification history available. Classify some text first!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Text Classification App v1.0")