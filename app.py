import os
import openai
import fitz 
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_file
from transformers import pipeline
from groq import Groq

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        openai_api_key = request.form['api_key']
        uploaded_file = request.files['pdf_file']
        jd_file = request.files.get('jd_file')

        if openai_api_key and uploaded_file:
            unique_filename = f'resume_{uuid.uuid4().hex}.html'
            pdf_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(pdf_path)

            extracted_text = extract_text_from_pdf(pdf_path)

            jd_text = None
            if jd_file:
                jd_path = os.path.join(UPLOAD_FOLDER, jd_file.filename)
                jd_file.save(jd_path)
                jd_text = extract_text_from_pdf(jd_path)

            # # Delete any existing resume.html files
            # for filename in os.listdir(UPLOAD_FOLDER):
            #     if filename.startswith('resume') and filename.endswith('.html'):
            #         os.remove(os.path.join(UPLOAD_FOLDER, filename))

            # # Generate a unique filename for the new resume
            # unique_filename = 'resume.html'
            html_resume = generate_html_resume(openai_api_key, extracted_text, jd_text)
            html_file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            with open(html_file_path, 'w') as f:
                f.write(html_resume)

            return redirect(url_for('download_resume', filename=unique_filename))

    return render_template('index.html')

@app.route('/download/<filename>')
def download_resume(filename):
    """Endpoint to download the generated resume."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        response = send_file(file_path, as_attachment=True)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except FileNotFoundError:
        return "Resume not found.", 404

def extract_text_from_pdf(pdf_path):
    """Extracts text from PDF using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_html_resume(api_key, text, jd_text=None):
    """Generate HTML resume using OpenAI API."""
    openai.api_key = api_key


    client = Groq(api_key="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")

    prompt = f"""
    <instruction>

    You are an expert resume generator and can only output html code.
    Convert the following extracted LinkedIn resume details into an HTML format, and make sure it is ATS (Applicant Tracking System) friendly. If job description text is provided, tailor the resume to highlight relevant experience. 
    It is your task to generate only and only the html code and do not give anything else as the output. Remember, you need to give only the html code and no description for it.

    </instruction>

    HTML format for the resume template:

    <format>

    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0 auto;
                padding: 0;
                width: 85%;
                color: #333;
            }}
            h1, h2, h3 {{
                color: #333;
                margin: 0;
                padding-bottom: 10px;
            }}
            h1 {{
                text-align: center;
                font-size: 28px;
                text-transform: uppercase;
            }}
            h2 {{
                font-size: 20px;
                border-bottom: 1px solid #ccc;
                margin-bottom: 10px;
            }}
            h3 {{
                font-size: 18px;
                margin-bottom: 5px;
            }}
            .contact-info {{
                text-align: center;
                margin-top: 5px;
                font-size: 14px;
            }}
            .contact-info a {{
                text-decoration: none;
                color: #333;
            }}
            ul {{
                list-style: none;
                padding: 0;
                margin: 0;
            }}
            li {{
                padding-bottom: 5px;
                margin-bottom: 5px;
            }}
            .section {{
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <!-- Contact Information -->
        <h1>First Last</h1>
        <p class="contact-info">
            123 Street Name, Town, State 12345 <br>
            <a href="tel:123-456-7890">123-456-7890</a> | 
            <a href="mailto:somebody@domain.com">somebody@domain.com</a> |
            <a href="https://linkedin.com/in/username">linkedin.com/in/username</a> |
            <a href="https://github.com/username">github.com/username</a>
        </p>

        <!-- Education Section -->
        <div class="section">
            <h2>Education</h2>
            <ul>
                <li><strong>University</strong>, Degree Name, State (Jan 2021 – Current)</li>
                <li><strong>Junior College Name</strong>, HSC Board, City, State (Sep 2017 – May 2021)</li>
                <li><strong>School Name</strong>, SSC, Board, City, State (Sep 2017 – May 2021)</li>
            </ul>
        </div>

        <!-- Relevant Coursework -->
        <div class="section">
            <h2>Relevant Coursework</h2>
            <ul>
                <li>Relevant Coursework 1</li>
                <li>Relevant Coursework 2</li>
                <li>Relevant Coursework 3</li>
                <li>Relevant Coursework 4</li>
                <li>Relevant Coursework 5</li>
                <li>Relevant Coursework 6</li>
            </ul>
        </div>

        <!-- Experience/Internships Section -->
        <div class="section">
            <h2>Experience/Internships</h2>
            <ul>
                <li>
                    <strong>Company Name</strong>, Position, City, State (May 2020 – August 2020)
                    <ul>
                        <li>Description line 1.</li>
                        <li>Description line 2.</li>
                        <li>Description line 3.</li>
                    </ul>
                </li>
                <li>
                    <strong>Company Name</strong>, Position, City, State (May 2020 – August 2020)
                    <ul>
                        <li>Description line 1.</li>
                        <li>Description line 2.</li>
                        <li>Description line 3.</li>
                    </ul>
                </li>
            </ul>
        </div>

        <!-- Projects Section -->
        <div class="section">
            <h2>Projects</h2>
            <ul>
                <li>
                    <strong>Project Name</strong> | Python, Selenium, Google Cloud Console (January 2021)
                    <ul>
                        <li>Description line 1.</li>
                        <li>Description line 2.</li>
                        <li>Description line 3.</li>
                    </ul>
                </li>
                <li>
                    <strong>Project Name</strong> | Python, Selenium, Google Cloud Console (January 2021)
                    <ul>
                        <li>Description line 1.</li>
                        <li>Description line 2.</li>
                        <li>Description line 3.</li>
                    </ul>
                </li>
            </ul>
        </div>

        <!-- Technical Skills Section -->
        <div class="section">
            <h2>Technical Skills</h2>
            <ul>
                <!-- Add Technical Skills Here -->
            </ul>
        </div>

        <!-- Leadership / Extracurricular Section -->
        <div class="section">
            <h2>Leadership / Extracurricular</h2>
            <ul>
                <li>
                    <strong>Name</strong>, President, University Name (Spring 2020 – Present)
                    <ul>
                        <li>Description line 1.</li>
                        <li>Description line 2.</li>
                        <li>Description line 3.</li>
                    </ul>
                </li>
            </ul>
        </div>
    </body>
    </html>

    </format>
    
    <content>

    Using this format, generate an HTML resume from the following extracted text. Ensure that the HTML is clean, readable, and ATS-compliant. Adjust or omit irrelevant sections if needed to fit the professional resume format:

    LinkedIn Text:
    {text}

    {"Job Description Text: " + jd_text if jd_text else ""}

    </content>

    <instruction>

    Note: Directly give the output html code and no description for it.
    Note: Make sure that the resume is complete.

    </instruction>
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']

    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"You are an expert in using html. All you do is this: generate correct html code for a professional resume. You are not a conversational model in this case but an html code generator. Generate an HTML formatted resume from the following text: {text}. It is your task to generate only and only the html code and do not give anything else as the output."
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return "Error generating resume due to an unexpected issue."

if __name__ == "__main__":
    app.run(debug=True)
else:
    app = app
