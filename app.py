import os
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import json

app = Flask(__name__)

# Load the saved model
def load_model():
    try:
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Initialize the model
model = load_model()

class MedicalSentimentAnalyzer:
    def __init__(self):
        """Initialize the medical sentiment and intent analyzer."""
        # Define sentiment and intent labels
        self.sentiment_labels = ["Anxious", "Neutral", "Reassured"]
        self.intent_labels = [
            "Seeking reassurance",
            "Reporting symptoms",
            "Expressing concern",
            "Requesting information",
            "Acknowledging improvement"
        ]

        # Rule-based features to augment model predictions
        self.anxiety_keywords = [
            "worried", "concerned", "anxious", "nervous", "fear", "afraid",
            "scared", "stress", "distress", "pain", "hurt", "unsure", "future"
        ]

        self.reassurance_keywords = [
            "relief", "better", "improving", "good", "great", "positive", "recover",
            "recovery", "progress", "fine", "okay", "ok", "hope", "encouraged"
        ]

        self.symptom_keywords = [
            "pain", "ache", "sore", "discomfort", "stiff", "tender",
            "hurt", "sensation", "feeling", "headache", "migraine", "nausea"
        ]

        self.body_parts = [
            "back", "neck", "head", "arm", "leg", "knee", "shoulder",
            "wrist", "ankle", "hip", "spine", "muscle", "joint"
        ]

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of patient text.
        """
        # Rule-based approach
        text_lower = text.lower()

        # Count anxiety and reassurance keywords
        anxiety_score = sum(1 for word in self.anxiety_keywords if word in text_lower)
        reassurance_score = sum(1 for word in self.reassurance_keywords if word in text_lower)

        # Implement rules for sentiment classification
        if "hope" in text_lower and any(word in text_lower for word in self.anxiety_keywords):
            return "Anxious"  # Hopeful but still anxious
        elif anxiety_score > reassurance_score:
            return "Anxious"
        elif reassurance_score > anxiety_score:
            return "Reassured"
        elif any(word in text_lower for word in ["worried", "concern", "fear", "afraid"]):
            return "Anxious"  # Key anxiety indicators
        elif any(word in text_lower for word in ["better", "good", "fine", "relief"]):
            return "Reassured"  # Key reassurance indicators
        else:
            return "Neutral"  # Default to neutral

    def detect_intent(self, text):
        """
        Detect the primary intent of patient text.
        """
        text_lower = text.lower()

        # Check for symptom reporting intent
        if any(symptom in text_lower for symptom in self.symptom_keywords) and \
           any(part in text_lower for part in self.body_parts):
            return "Reporting symptoms"

        # Check for seeking reassurance intent
        if any(word in text_lower for word in ["will", "hope", "get", "better"]) and \
           any(word in text_lower for word in self.anxiety_keywords):
            return "Seeking reassurance"

        # Check for expressing concern
        if any(word in text_lower for word in ["worried", "concerned", "anxious"]):
            return "Expressing concern"

        # Check for requesting information
        if any(word in text_lower for word in ["?", "what", "when", "how", "why", "tell"]):
            return "Requesting information"

        # Check for acknowledging improvement
        if any(word in text_lower for word in ["better", "improving", "good", "fine", "recovered"]):
            return "Acknowledging improvement"

        # Default to most common intent in medical contexts
        return "Reporting symptoms"

    def analyze_patient_dialogue(self, text):
        """
        Analyze patient dialogue for sentiment and intent.
        """
        sentiment = self.analyze_sentiment(text)
        intent = self.detect_intent(text)

        return {
            "Sentiment": sentiment,
            "Intent": intent
        }

def extract_patient_dialogues(transcript):
    """
    Extract only the patient's dialogues from the full transcript.
    """
    lines = transcript.strip().split('\n')
    patient_dialogues = []

    for line in lines:
        # Modified to be more flexible in matching patient utterances
        if line.strip().startswith("Patient:"):
            # Extract only the patient's speech, removing the "Patient:" prefix
            dialogue = line.replace("Patient:", "").strip()
            patient_dialogues.append(dialogue)

    return patient_dialogues

def analyze_medical_conversation(transcript):
    """
    Analyze a medical conversation transcript for patient sentiment and intent.
    """
    # Extract patient dialogues
    patient_dialogues = extract_patient_dialogues(transcript)

    # Initialize the analyzer
    analyzer = MedicalSentimentAnalyzer()

    # Analyze each patient utterance
    utterance_analyses = []
    for dialogue in patient_dialogues:
        analysis = analyzer.analyze_patient_dialogue(dialogue)
        utterance_analyses.append({
            "Utterance": dialogue,
            "Analysis": analysis
        })

    # Determine overall sentiment and intent
    sentiment_counts = {}
    intent_counts = {}

    for analysis in utterance_analyses:
        sentiment = analysis["Analysis"]["Sentiment"]
        intent = analysis["Analysis"]["Intent"]

        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    # Get most common sentiment and intent
    overall_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])[0] if sentiment_counts else "Neutral"
    overall_intent = max(intent_counts.items(), key=lambda x: x[1])[0] if intent_counts else "Reporting symptoms"

    # Prepare results
    results = {
        "Overall_Analysis": {
            "Sentiment": overall_sentiment,
            "Intent": overall_intent
        },
        "Utterance_Analyses": utterance_analyses
    }

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        data = request.json
        transcript = data.get('transcript', '')
        
        # Analyze the transcript
        analysis_results = analyze_medical_conversation(transcript)
        
        return jsonify(analysis_results)

if __name__ == '__main__':
    # Use environment variable for port if available (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)