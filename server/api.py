import os
import re
import joblib
import sklearn
import psycopg2

from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor

load_dotenv()

# flask setup -----
app = Flask(__name__)
CORS(app)

# connect to database -----
def get_connection():
    try:
        conn = psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            dbname=os.getenv("dbname")
        )
        return conn
    except Exception as e:
        print("Failed to connect to the database:", e)
        raise  # re-raise the exception for further debugging


# load trained pipeline -----
model = joblib.load("model.joblib")
print("[DEBUG] model loaded:", type(model)) # should print sklearn.pipeline.Pipeline

# preprocessing -----
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
    "weren't", 'won', "won't", 'wouldn', "wouldn't", "im", "ive", "ill", "id", "its", "itll", "itd", "hes", "hell", "hed", "shes",
    "shell", "shed", "were", "weve", "well", "wed", "theyre", "theyve", "theyll", "theyd", "youre", "youll", "youve", "youd",
    'dont', 'cant', 'couldnt', 'didnt', 'doesnt', 'hadnt', 'hasnt', 'havent', 'isnt', 'mightnt', 'mustnt', 'neednt', 'shant'
]

# clean text -----
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]+', '', text)
    text = ' '.join([w for w in text.split() if w not in custom_stopwords])
    return text

# classify text -----
@app.route("/api/predict", methods=["POST"])
def classify_text():
    try:
        data = request.get_json(force=True)
        raw_text = data.get("text", "").strip()
        if not raw_text:
            return jsonify({"error": "No text provided"}), 400

        prepped_text = clean_text(raw_text)
        prediction = model.predict([prepped_text])[0]
        proba = model.predict_proba([prepped_text])[0]
        confidence = round(100 * max(proba), 2)
        label = "Normal Text" if prediction == 0 else "Mental Health-related Text"

        # with get_connection() as conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute('''
        #             INSERT INTO classification_history 
        #             (text, prediction, label, confidence)
        #             VALUES (%s, %s, %s, %s)
        #         ''', (raw_text, int(prediction), label, confidence))
        #         conn.commit()

        return jsonify({
            "prediction": int(prediction),
            "label": label,
            "confidence": confidence
        })
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": "Server crashed", "details": str(e)}), 500

# history section -----
# @app.route("/api/history", methods=["GET"])


# health check -----
@app.route("/api/ping")
def ping():
    return "pong"

# user Section
def get_table_list():
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                return cursor.fetchall()
    except Exception as e:
        print(f"Failed to fetch table list: {e}")
        return []

# fetch all rows from a given table
def fetch_table_data(table_name):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f'SELECT * FROM "{table_name}";')
                return cursor.fetchall()
    except Exception as e:
        return {"error": str(e)}

# API: Get all data from all tables
@app.route('/data', methods=['GET'])
def get_all_data():
    tables = get_table_list()
    data = {}
    for table in tables:
        table_name = table['table_name']
        data[table_name] = fetch_table_data(table_name)
    return jsonify(data)

# API: Get all table names
@app.route('/getAllTable', methods=['GET'])
def get_all_table():
    tables = get_table_list()
    return jsonify({"tables": [table['table_name'] for table in tables]})

# API: Debug prints tables to console
@app.route('/debug', methods=['POST'])
def debug():
    tables = get_table_list()
    print("Tables in database:")
    for table in tables:
        print(table['table_name'])
    return jsonify({"debug": "Printed to console"})



if __name__ == "__main__":
    app.run(debug=True, port=8080)