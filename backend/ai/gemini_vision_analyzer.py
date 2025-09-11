import google.generativeai as genai
from PIL import Image
import os

class GeminiVisionAnalyzer:
    """
    Analyzes inventory documents (images, PDFs) using the Gemini Vision API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the analyzer and configures the Gemini API.
        """
        if not api_key:
            raise ValueError("API key must be provided.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def analyze_document(self, file_path: str, prompt: str) -> str:
        """
        Analyzes a document file using the Gemini Vision model.

        Args:
            file_path: The path to the document file.
            prompt: The prompt to guide the analysis.

        Returns:
            The raw text result from the model.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file was not found at {file_path}")

        try:
            img = Image.open(file_path)
            
            # Generate content using the image and the prompt
            response = self.model.generate_content([prompt, img])
            
            return response.text
        except Exception as e:
            print(f"An error occurred during Gemini analysis: {e}")
            raise
