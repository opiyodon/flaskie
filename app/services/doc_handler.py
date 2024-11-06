from pdfminer.high_level import extract_text as pdf_extract
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
import os

def process_document(filepath):
    """Process different types of documents and extract text/data."""
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == '.pdf':
            return process_pdf(filepath)
        elif ext == '.docx':
            return process_docx(filepath)
        elif ext == '.xlsx':
            return process_xlsx(filepath)
        elif ext == '.pptx':
            return process_pptx(filepath)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        raise Exception(f"Error processing document: {str(e)}")

def process_pdf(filepath):
    """Extract text from PDF file."""
    text = pdf_extract(filepath)
    return {
        "type": "pdf",
        "content": text,
        "pages": len(text.split('\f')),  # Rough page count
        "word_count": len(text.split())
    }

def process_docx(filepath):
    """Extract text and metadata from DOCX file."""
    doc = Document(filepath)
    paragraphs = [p.text for p in doc.paragraphs]
    
    return {
        "type": "docx",
        "content": "\n".join(paragraphs),
        "paragraphs": len(paragraphs),
        "word_count": sum(len(p.split()) for p in paragraphs)
    }

def process_xlsx(filepath):
    """Extract data from Excel file."""
    wb = load_workbook(filepath, read_only=True)
    sheets_data = {}
    
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        data = []
        for row in ws.iter_rows(values_only=True):
            data.append([str(cell) if cell is not None else "" for cell in row])
        sheets_data[sheet] = data
    
    return {
        "type": "xlsx",
        "sheets": sheets_data,
        "sheet_count": len(sheets_data)
    }

def process_pptx(filepath):
    """Extract text from PowerPoint file."""
    prs = Presentation(filepath)
    slides_data = []
    
    for slide in prs.slides:
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text.append(shape.text)
        slides_data.append("\n".join(slide_text))
    
    return {
        "type": "pptx",
        "slides": slides_data,
        "slide_count": len(slides_data)
    }
