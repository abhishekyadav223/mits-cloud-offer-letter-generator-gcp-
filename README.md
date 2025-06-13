MITS Cloud Offer Letter Generator

📝 Description

A serverless web application built using Google Cloud Functions, SendGrid, and HTML/CSS/JS that allows internship applicants to receive a dynamically generated PDF offer letter by email.


---

🌐 Live Demo

[Visit Live Form](https://storage.googleapis.com/mits-intern-site/index.html)


---

✨ Features

📄 Generate internship offer letters as PDFs

📬 Automatically emails the letter to the applicant

✅ Validates form input before submission

☁️ Fully serverless with scalable deployment

🛡️ Supports CORS and secure API handling



---

📦 Technologies Used

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask via Cloud Function)

PDF Generator: ReportLab

Email Service: SendGrid API

Hosting: Google Cloud Storage (for HTML)

Deployment: Google Cloud Functions (Gen 2)



---

🗂️ Project Structure

.
├── index.html                   # User-facing frontend form
├── main.py                     # Backend logic (PDF + Email)
├── requirements.txt            # Python dependencies
└── mits_offer_letter_function/ # Folder for deployment to Cloud


---

🚀 Deployment Instructions

🔹 Google Cloud Function

1. Enable Cloud Functions, Cloud Build, Artifact Registry, and IAM APIs


2. Create a Cloud Function:



gcloud functions deploy generate_offer_letter \
  --runtime python310 \
  --trigger-http \
  --entry-point generate_offer_letter \
  --region=us-central1 \
  --allow-unauthenticated \
  --source .

🔹 SendGrid Setup

1. Create a SendGrid account


2. Generate a Full Access API Key


3. Verify sender email (Single Sender Verification)


4. Paste API key in main.py:



SENDGRID_API_KEY = "your-sendgrid-api-key"

5. Set the same email in from_email as verified




---

