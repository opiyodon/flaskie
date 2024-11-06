from PIL import Image
import pytesseract
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

def extract_text_from_image(image_path):
    """Extract text from image using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return {
            "text": text,
            "word_count": len(text.split()),
            "language": pytesseract.image_to_osd(image)
        }
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

def generate_word_cloud(text):
    """Generate word cloud from text."""
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white'
        ).generate(text)
        
        # Save word cloud to bytes
        img_bytes = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img_bytes, format='PNG')
        plt.close()
        
        return {
            "image": base64.b64encode(img_bytes.getvalue()).decode('utf-8'),
            "format": "PNG",
            "word_count": len(text.split())
        }
    except Exception as e:
        raise Exception(f"Error generating word cloud: {str(e)}")

def analyze_image(image_path):
    """Analyze image properties."""
    try:
        with Image.open(image_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "info": img.info
            }
    except Exception as e:
        raise Exception(f"Error analyzing image: {str(e)}")
