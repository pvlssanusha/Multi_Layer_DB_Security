import pickle
import os
import re

BASE_DIR = os.path.dirname(__file__)

# # Load model
# with open(os.path.join(BASE_DIR, "sqli_model.pkl"), "rb") as f:
#     model = pickle.load(f)

# with open(os.path.join(BASE_DIR, "sqli_vectorizer.pkl"), "rb") as f:
#     vectorizer = pickle.load(f)

with open(os.path.join(BASE_DIR, "rf_model.pkl"), "rb") as f:
    model = pickle.load(f) # Load vectorizer
with open(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"), "rb") as f: 
    vectorizer = pickle.load(f)
# 🔒 Rule-based detection (fast + reliable)
def rule_based_check(text):
    text = str(text).lower()

    patterns = [
        r"drop\s+table",
        r"delete\s+from",
        r"insert\s+into",
        r"update\s+.*set",
        r"alter\s+table",
        r"union\s+select",
        r"or\s+1=1",
        r"'--",
        r"--",
        r";--",
        r"/\*.*\*/"
    ]

    for pattern in patterns:
        if re.search(pattern, text):
            return True

    return False

def predict_query(query_text): 
    """ Predict if query is malicious """
     # Convert to TF-IDF
    if rule_based_check(query_text):
        return True, 1.0
    vector = vectorizer.transform([query_text]) 
     # # Prediction
    prediction = model.predict(vector)[0]  
    #Confidence
    print("prediction prob",prediction) 
    confidence = max(model.predict_proba(vector)[0])
    
    print("predicting",prediction==1,"confidence",confidence)
    return prediction == 1, confidence