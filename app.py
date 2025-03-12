from dotenv import load_dotenv 
load_dotenv()
import streamlit as st
import io
import base64
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
from pdf2image import convert_from_bytes

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the latest model
model = genai.GenerativeModel("gemini-1.5-flash")

# Convert PDF to Image
def input_pdf_setup(upload_file):
    if upload_file is not None:
        images = pdf2image.convert_from_bytes(
            upload_file.read(),
            poppler_path=r"C:\Users\Rohit Bisht\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
        )
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",  # ✅ Correct MIME type
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to get Gemini Response
def get_gemini_response(input_prompt, pdf_content, job_description):
    model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Latest model
    response = model.generate_content([input_prompt, pdf_content[0], job_description])
    return response.text

# Streamlit App
st.set_page_config(page_title="AI-powered Resume Analyzer")
st.header("ATS Tracking System")

# User Input
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Submit Button
submit1 = st.button("Tell Me About The Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with tech experience in Data Science, Full Stack Web Development, 
Big Data Engineering, DevOps, and Data Analysis. Review the provided resume against the job description.
Highlight strengths and weaknesses.
"""

input_prompt3 = """
You are an ATS (Applicant Tracking System) scanner with expertise in Web Development, Big Data Engineering, 
DevOps, and Data Analysis. Evaluate the resume against the job description and provide a match percentage 
along with keyword insights.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
