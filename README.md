## General
A simple website to classify whether a text is mental health related or not.
The website is coded using react for frontend and flask for backend.
And then it uses machine learning model to classify the text, in this case it uses voting classifier.
The main problem is it does not have a login nor register features, so every text written will be stored in a single database and everyone can see the history.

## Files & Folders
- Frontend -> contains the source files such as assets, components, and page
- Server -> contains the backend (api.py) and model used (.joblib)
- Python Notebook -> the models tested from voting classifier to lstm (model_selection.ipynb) 

## Features
- Classify text using a machine learning model
- View history of previous classifications
- Delete text in history (delete single or all)
- User-friendly interface??

## Notes
Update - 22/5/2025 - Done?? Maybe...
Update 2.0 - 26/5/2025 - Done???

## How to use
### Clone repo in cmd
```
git clone https://github.com/yoru0/Mental-Health-Classification.git
```

### Run frontend
```
cd frontend
npm install
npm run dev
```
Then copy the localhost and paste it on your browser

### Run server
```
cd server
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python api.py
```