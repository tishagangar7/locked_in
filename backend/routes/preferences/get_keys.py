import google.generativeai as genai
import os
import pypdf
from pdf2image import convert_from_path
import pytesseract

# Configure the Generative AI API
genai.configure(api_key=os.environ.get("GENAI_API_KEY", "your_api_key_here"))

# Function to load text files
def load_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading text file {filepath}: {e}")
        return None

# Function to load PDF files
def load_pdf_text(filepath):
    text = ""
    try:
        reader = pypdf.PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Add newline between pages
        if not text.strip():  # If no text was extracted, use OCR
            print("No text found in PDF. Falling back to OCR...")
            images = convert_from_path(filepath)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF file {filepath}: {e}")
        return None

# Simple prompt for extracting topics and keywords
prompt_simple = f"""
Analyze the following syllabus text and extract the main topics and keywords discussed.
Provide the output as a clean list.

Syllabus Text:
---
{{syllabus_text}}
---

Topics and Keywords:
"""

# Structured prompt for extracting detailed information in JSON format
prompt_structured = f"""
Act as an academic assistant analyzing a course syllabus.
From the syllabus text provided below, identify:
1.  The main topics covered, ideally based on a weekly schedule if present.
2.  Key concepts, theories, or specific terminology mentioned.
3.  Any software, tools, or techniques explicitly listed.

Present the output in JSON format with keys: "weekly_topics" (list of strings or objects with week/topic), "key_concepts" (list of strings), and "tools_techniques" (list of strings).

Syllabus Text:
---
{{syllabus_text}}
---

JSON Output:
```json
"""

# Function to process the syllabus and extract data
def process_syllabus(filepath, use_structured_prompt=True):
    syllabus_content = load_text(filepath) if filepath.endswith('.txt') else load_pdf_text(filepath)
    if not syllabus_content:
        print("Syllabus content could not be loaded.")
        return None

    # Choose the appropriate prompt
    if use_structured_prompt:
        final_prompt = prompt_structured.format(syllabus_text=syllabus_content)
        final_prompt += "```json\n"  # Add JSON hint for structured output
    else:
        final_prompt = prompt_simple.format(syllabus_text=syllabus_content)

    try:
        # Configure generation settings
        generation_config = genai.types.GenerationConfig(
            temperature=0.2  # Lower temperature for more deterministic output
        )

        # Choose a model (e.g., 'gemini-1.5-flash')
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content using the AI model
        response = model.generate_content(final_prompt, generation_config=generation_config)

        # Handle response
        if response.parts:
            extracted_data = response.text
            # Clean JSON wrapper if using structured prompt
            if use_structured_prompt and "```json" in final_prompt:
                extracted_data = extracted_data.strip().lstrip('```json').rstrip('```')
            return extracted_data
        else:
            print("Warning: Received empty response or content was blocked.")
            print(response.prompt_feedback)  # Check for safety issues
            return None

    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return None

# Main function for testing
if __name__ == "__main__":
    # Example usage
    filepath = "./syllabus.txt"  # Replace with the path to your syllabus file
    use_structured_prompt = True  # Set to False for simple keyword extraction

    extracted_data = process_syllabus(filepath, use_structured_prompt=use_structured_prompt)

    if extracted_data:
        print("Processing complete. Extracted data:")
        print(extracted_data)
    else:
        print("Failed to process the syllabus.")