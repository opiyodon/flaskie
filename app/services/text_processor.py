from functools import lru_cache
import gc
import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download, FreqDist
import nltk

# Download NLTK data during initialization
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    download('punkt')
    download('stopwords')

class TextProcessor:
    def __init__(self):
        self._sentiment_analyzer = None
        self._summarizer = None
        self._stop_words = set(stopwords.words('english'))

    @lru_cache(maxsize=128)
    def _get_sentiment_analyzer(self):
        """Lazy load sentiment analyzer with a smaller model."""
        if self._sentiment_analyzer is None:
            # Use a smaller model for sentiment analysis
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            self._sentiment_analyzer = pipeline(
                'sentiment-analysis',
                model=model_name,
                device=-1  # Force CPU usage
            )
        return self._sentiment_analyzer

    @lru_cache(maxsize=128)
    def _get_summarizer(self):
        """Lazy load summarizer with a smaller model."""
        if self._summarizer is None:
            # Use a smaller model for summarization
            model_name = "facebook/bart-large-cnn"
            self._summarizer = pipeline(
                'summarization',
                model=model_name,
                device=-1  # Force CPU usage
            )
        return self._summarizer

    def _clear_gpu_memory(self):
        """Clear GPU memory after processing."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the given text."""
        try:
            analyzer = self._get_sentiment_analyzer()
            result = analyzer(text[:512])[0]  # Limit input length
            
            sentiment_result = {
                "sentiment": result['label'],
                "confidence": round(result['score'], 4)
            }
            
            self._clear_gpu_memory()
            return sentiment_result
        
        except Exception as e:
            return {
                "error": f"Sentiment analysis failed: {str(e)}",
                "sentiment": "UNKNOWN",
                "confidence": 0.0
            }

    def generate_summary(self, text, max_length=130, min_length=30):
        """Generate a summary of the given text."""
        try:
            # Only process if text is long enough to summarize
            if len(text.split()) < min_length:
                return {
                    "summary": text,
                    "original_length": len(text.split()),
                    "summary_length": len(text.split())
                }

            summarizer = self._get_summarizer()
            
            # Chunk text if it's too long
            max_input_length = 1024
            text = text[:max_input_length]
            
            summary = summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            
            summary_result = {
                "summary": summary[0]['summary_text'],
                "original_length": len(text.split()),
                "summary_length": len(summary[0]['summary_text'].split())
            }
            
            self._clear_gpu_memory()
            return summary_result
            
        except Exception as e:
            return {
                "error": f"Summarization failed: {str(e)}",
                "summary": text,
                "original_length": len(text.split()),
                "summary_length": len(text.split())
            }

    @lru_cache(maxsize=256)
    def extract_keywords(self, text, num_keywords=10):
        """Extract key phrases from the text."""
        try:
            # Tokenize and remove stopwords
            tokens = word_tokenize(text.lower())
            keywords = [word for word in tokens 
                       if word.isalnum() and word not in self._stop_words]
            
            # Count frequency
            freq_dist = FreqDist(keywords)
            
            return {
                "keywords": [
                    {"word": word, "count": count}
                    for word, count in freq_dist.most_common(num_keywords)
                ]
            }
            
        except Exception as e:
            return {
                "error": f"Keyword extraction failed: {str(e)}",
                "keywords": []
            }

    def cleanup(self):
        """Cleanup method to be called when shutting down."""
        self._sentiment_analyzer = None
        self._summarizer = None
        self._clear_gpu_memory()

# Create a singleton instance
text_processor = TextProcessor()

# Export functions that maintain the original API
def analyze_sentiment(text):
    return text_processor.analyze_sentiment(text)

def generate_summary(text, max_length=130, min_length=30):
    return text_processor.generate_summary(text, max_length, min_length)

def extract_keywords(text, num_keywords=10):
    return text_processor.extract_keywords(text, num_keywords)