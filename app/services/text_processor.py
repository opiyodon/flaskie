from transformers import pipeline
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
import nltk
from cachetools import TTLCache

class TextProcessor:
    def __init__(self):
        # Download required NLTK data
        download('punkt')
        download('stopwords')
        
        # Initialize transformers
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        self.summarizer = pipeline('summarization')
        
        # Initialize cache
        self.cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour cache

    def analyze_sentiment(self, text):
        cache_key = f"sentiment_{hash(text)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.sentiment_analyzer(text[:512])[0]  # Limit text length
        
        processed_result = {
            'sentiment': result['label'],
            'confidence': round(result['score'], 4)
        }
        
        self.cache[cache_key] = processed_result
        return processed_result

    def generate_summary(self, text):
        cache_key = f"summary_{hash(text)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Split long text into chunks if necessary
        max_chunk_size = 1024
        if len(text) > max_chunk_size:
            chunks = [text[i:i + max_chunk_size] 
                     for i in range(0, len(text), max_chunk_size)]
            summaries = []
            for chunk in chunks:
                summary = self.summarizer(chunk, 
                                        max_length=130, 
                                        min_length=30, 
                                        do_sample=False)
                summaries.append(summary[0]['summary_text'])
            result = ' '.join(summaries)
        else:
            summary = self.summarizer(text, 
                                    max_length=130, 
                                    min_length=30, 
                                    do_sample=False)
            result = summary[0]['summary_text']
        
        processed_result = {
            'summary': result
        }
        
        self.cache[cache_key] = processed_result
        return processed_result

    def extract_keywords(self, text):
        cache_key = f"keywords_{hash(text)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        keywords = [token for token in tokens 
                   if token.isalnum() and token not in stop_words]
        
        # Get frequency distribution
        freq_dist = nltk.FreqDist(keywords)
        
        # Get top 10 keywords
        top_keywords = [{'word': word, 'frequency': freq} 
                       for word, freq in freq_dist.most_common(10)]
        
        processed_result = {
            'keywords': top_keywords
        }
        
        self.cache[cache_key] = processed_result
        return processed_result
