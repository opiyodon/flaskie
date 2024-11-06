from transformers import pipeline
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
import nltk

# Download required NLTK data
download('punkt')
download('stopwords')

# Initialize transformers
sentiment_analyzer = pipeline('sentiment-analysis')
summarizer = pipeline('summarization')

def analyze_sentiment(text):
    """Analyze the sentiment of the given text."""
    result = sentiment_analyzer(text)[0]
    return {
        "sentiment": result['label'],
        "confidence": round(result['score'], 4)
    }

def generate_summary(text, max_length=130, min_length=30):
    """Generate a summary of the given text."""
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return {
        "summary": summary[0]['summary_text'],
        "original_length": len(text.split()),
        "summary_length": len(summary[0]['summary_text'].split())
    }

def extract_keywords(text, num_keywords=10):
    """Extract key phrases from the text."""
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Count frequency
    freq_dist = nltk.FreqDist(keywords)
    
    return {
        "keywords": [{"word": word, "count": count} 
                    for word, count in freq_dist.most_common(num_keywords)]
    }
