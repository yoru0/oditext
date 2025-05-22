# General
A simple website to classify whether a text is mental health related or not.
The website is coded using react for frontend and flask for backend.
And then it uses machine learning model to classify the text, in this case it uses logistic regression with around 92% test accuracy.
The main problem is it does not have a login nor register features, so every text written will be stored in a single database and everyone can see the history.

## Features
- Classify text using a machine learning model
- View history of previous classifications
- Delete text in history
- User-friendly interface??

## Notes
CoNfUsEd. I dOnT uNdErStAnD.

Update - 5/22/2025 - Done?? Maybe...

## How to use
Clone the repo
```
git clone https://github.com/yoru0/Mental-Health-Classification.git
```

Run frontend
```
cd frontend
```
```
npm install
```
```
npm run dev
```
And then just copy the local host and paste it on your browser

Run server
```
cd server
```
```
venv/Scripts/activate
```
```
python api.py
```