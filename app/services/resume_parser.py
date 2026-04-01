import io
from pypdf import PdfReader
import docx

def parse_resume_file(filename: str, file_content: bytes) -> str:
    """
    Parses PDF or DOCX file content and returns extracted text.
    Hackathon friendly: memory based, no temp files needed.
    """
    ext = filename.split(".")[-1].lower()
    text = ""
    
    try:
        if ext == "pdf":
            reader = PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        elif ext in ["doc", "docx"]:
            doc = docx.Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""
        
    return text.strip()
