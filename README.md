# LinkedIn PDF to HTML Resume Generator

## Description

The **LinkedIn PDF to HTML Resume Generator** is a web application that provides the conversion of LinkedIn PDF profiles into professional, HTML-based resumes. The app integrates with OpenAI’s GPT-4 API for resume generation, with Llama as a backup when OpenAI API credits are exhausted. The application uses prompt engineering with tag-based enhancements to ensure the resumes are well-structured and relevant.

### Key Features

1. **LinkedIn PDF Upload**: Users can upload their LinkedIn profile in PDF format. The application extracts the text for further processing.
   
2. **OpenAI and Llama Integration**: The extracted data is processed using OpenAI’s GPT-4 to generate a structured HTML resume. In case OpenAI API credits are unavailable, the Llama model is used to maintain functionality.
   
3. **Prompt Engineering with Tags**: Advanced prompt engineering is used to guide the AI in crafting optimized resumes, utilizing tags to fine-tune the output for relevance and clarity.
   
4. **ATS-Friendly HTML Output**: The generated resume follows an ATS (Applicant Tracking System) compatible HTML format, ensuring it meets the standards for automated screening tools used by employers.

5. **Fallback Mechanism**: When OpenAI credits run out, the app automatically switches to using the Llama model to maintain continuous service.

### How It Works

1. **Upload LinkedIn PDF**: Users upload their LinkedIn profile as a PDF file.
   
2. **Text Extraction**: The application extracts text from the PDF using tools like PyPDF2 or similar libraries.
   
3. **AI-Powered Resume Generation**: OpenAI’s GPT-4 model processes the text to generate a tailored, ATS-compliant resume. If OpenAI credits are exhausted, the Llama model takes over seamlessly.
   
4. **Optimized Prompt Engineering**: The app applies prompt engineering strategies using specific tags to refine the results and ensure high-quality resumes.

5. **Resume in HTML Format**: The generated resume is saved and provided to users in an HTML format, which can be downloaded and further customized if needed.


## Installation and Setup

### Requirements

- Python 3.6+
- Flask
- PyMuPDF (Fitz)
- OpenAI API Key
- Transformers library for Llama model

### Steps to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/linkedin_resume_generator.git
   cd linkedin_resume_generator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key**:
   You need to have an OpenAI API key to use the GPT-4 model for generating the resume. You can get the API key from OpenAI.

4. **Run the Application**:
   ```bash
   flask run
   ```

5. **Access the Application**:
    Open your web browser and navigate to http://127.0.0.1:5000/ to use the application.