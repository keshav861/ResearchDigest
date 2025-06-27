import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")

# This will be updated when the user provides their API key
if api_key and api_key != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring Gemini API: {e}", file=sys.stderr)

# Default model to use - updated to the newer model version
DEFAULT_MODEL = "gemini-1.5-flash"

def generate_summary(title, abstract, max_chars=500):
    """
    Generate a 1-2 paragraph summary of a research paper using Gemini API
    
    Args:
        title (str): Title of the paper
        abstract (str): Abstract of the paper
        max_chars (int): Maximum character length for the summary
        
    Returns:
        str: The generated summary
    """
    # Check if API key is configured
    if not api_key or api_key == "your_gemini_api_key_here":
        return "Please configure your Gemini API key to enable summarization."
    
    try:
        # Create the prompt for Gemini
        prompt = f"""
        Summarize the following research paper in 1-2 clear, informative paragraphs:
        
        Title: {title}
        
        Abstract: {abstract}
        
        Provide a concise summary that captures the main points, methodology, and key findings.
        Focus on readability and information density.
        """
        
        # Initialize Gemini model with the updated model name
        model = genai.GenerativeModel(DEFAULT_MODEL)
        
        # Configure generation parameters
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 500,
        }
        
        # Generate response with better configuration
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Extract and clean the summary
        summary = response.text.strip()
        
        # Truncate if needed
        if len(summary) > max_chars:
            summary = summary[:max_chars] + "..."
            
        return summary
    
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}", file=sys.stderr)
        return f"Error generating summary: {str(e)[:100]}...\nPlease try again later."