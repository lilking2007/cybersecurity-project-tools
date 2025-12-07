# 🛡️ AI Phishing Email Detector

A machine learning-powered application designed to analyze email content and detect potential phishing attempts. This tool uses Natural Language Processing (NLP) techniques to identify suspicious patterns, malicious URLs, and urgent cues commonly found in phishing attacks.

## 🚀 Key Features

*   **Real-time Analysis**: Instant feedback on whether an email is likely "Safe" or "Phishing".
*   **Confidence Score**: Displays a probability percentage for the prediction.
*   **Heuristic Insights**: Highlights specific risk factors like suspicious keywords (e.g., "urgent", "verify") and URL counts.
*   **Modern UI**: Built with Streamlit for a clean, responsive, and user-friendly interface.

## 🛠️ How It Works

The project works in two main stages: **Training** and **Inference**.

### 1. The Model (Backend)
*   **Algorithm**: We use a **Random Forest Classifier**, a robust ensemble learning method.
*   **Feature Extraction**:
    *   **TF-IDF (Term Frequency-Inverse Document Frequency)**: Converts email text into numerical vectors, evaluating the importance of words relative to the dataset.
    *   **Metadata Extraction**: Analyzes auxiliary features such as the number of URLs and presence of high-risk keywords.
*   **Data Source**: The system currently generates synthetic training data mimicking common phishing and safe email patterns (handled in `src/utils.py`) to bootstrap the model without needing an external dataset immediately.

### 2. The Application (Frontend)
*   **Streamlit**: The web interface allows users to paste email content directly.
*   **Process**:
    1.  The app loads the pre-trained model (`models/phishing_model.pkl`).
    2.  User inputs text.
    3.  The text is passed through the preprocessing pipeline.
    4.  The model predicts the class (Safe vs. Phishing) and the confidence level.

## 📂 Project Structure

```text
Email_phishing_detection/
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── models/                 # specific directory for saved models
│   └── phishing_model.pkl  # The trained serialized model
├── src/                    # Source code for logic
│   ├── features.py         # Feature extraction pipelines
│   ├── model.py            # Model training and prediction functions
│   └── utils.py            # Data loading and synthetic data generation
└── data/                   # Directory for raw data (optional/future use)
```

## 💻 Installation & Usage

### Prerequisites
*   Python 3.8 or higher
*   pip (Python package manager)

### Step 1: Clone or Download
Ensure you have the project files on your local machine.

### Step 2: Install Dependencies
Navigate to the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 3: Train the Model
Before running the app for the first time, you must train the model to generate the `.pkl` file:
```bash
python src/model.py
```
*You should see output indicating the model accuracy and that it has been saved to `models/phishing_model.pkl`.*

### Step 4: Run the Application
Launch the Streamlit interface:
```bash
streamlit run app.py
```
A browser window should automatically open pointing to `http://localhost:8501`.

## 🛡️ Example Usage

**Try pasting this (Phishing Example):**
> "URGENT: Your account has been suspended due to suspicious activity. Click here http://bit.ly/fake-link to verify your identity immediately or you will lose access."

**Try pasting this (Safe Example):**
> "Hi team, just a reminder about the meeting tomorrow at 10 AM. I've attached the agenda for your review. Thanks!"

## 🤝 Contributing
Feel free to improve the `generate_dummy_data` function in `src/utils.py` to add more diverse training examples, or swap it out for a real-world dataset (like the Enron email dataset or similar phishing corpora).
