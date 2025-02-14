import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Load the saved vectorizer and model
with open(r'C:\Users\aniru\OneDrive\Desktop\New folder (2)\New folder (2)\vectorizer.pkl','rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

with open(r'C:\Users\aniru\OneDrive\Desktop\New folder (2)\New folder (2)\model.pkl','rb') as model_file:
    model = pickle.load(model_file)

def preprocess_url(url):
    """Preprocess the given URL."""
    from nltk.tokenize import RegexpTokenizer
    from nltk.stem.snowball import SnowballStemmer

    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    stemmer = SnowballStemmer("english")

    # Tokenize, stem, and join the tokens
    tokens = tokenizer.tokenize(url)
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(stemmed_tokens)

def classify_url():
    """Classify the URL entered by the user."""
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    try:
        # Preprocess the URL
        preprocessed_url = preprocess_url(url)

        # Convert the preprocessed text into vectorized form
        vectorized_url = vectorizer.transform([preprocessed_url])

        # Predict using the loaded model
        prediction = model.predict(vectorized_url)[0]

        # Display the result
        result_label.config(text=f"Prediction: {'Bad' if prediction == 'bad' else 'Good'}", fg="green" if prediction == 'good' else "red")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Phishing Website Detector")

# Set up the UI components
tk.Label(root, text="Enter Website URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

classify_button = tk.Button(root, text="Classify", font=("Arial", 12), command=classify_url)
classify_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
