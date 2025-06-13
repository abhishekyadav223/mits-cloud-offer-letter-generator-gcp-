import functions_framework
from flask import request, make_response
from io import BytesIO
from reportlab.pdfgen import canvas
import sendgrid
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import logging
import traceback

SENDGRID_API_KEY = "enter ut key"

@functions_framework.http
def generate_offer_letter(request):
    logging.info("Function triggered")
    
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    try:
        req_json = request.get_json(silent=True)
        logging.info(f"Received JSON: {req_json}")

        if not req_json:
            raise ValueError("Invalid request body")

        name = req_json.get('name')
        college = req_json.get('college')
        domain = req_json.get('domain')
        email = req_json.get('email')

        if not all([name, college, domain, email]):
            raise ValueError("Missing required fields")

        logging.info("Generating PDF...")
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "Micro Information Technology Services (MITS)")
        p.drawString(100, 780, "Offer Letter")
        p.drawString(100, 740, f"Dear {name},")
        p.drawString(100, 720, f"You have been selected for an internship in {domain}.")
        p.drawString(100, 700, f"College: {college}")
        p.drawString(100, 680, "Duration: 1 Month (Remote)")
        p.drawString(100, 660, "Wishing you a great learning experience!")
        p.drawString(100, 640, "- MITS Team")
        p.showPage()
        p.save()
        buffer.seek(0)
        pdf_data = buffer.read()

        logging.info("Preparing to send email...")
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        encoded_file = base64.b64encode(pdf_data).decode()

        attachment = Attachment()
        attachment.file_content = FileContent(encoded_file)
        attachment.file_type = FileType('application/pdf')
        attachment.file_name = FileName(f'offer_letter_{name.lower().replace(" ", "_")}.pdf')
        attachment.disposition = Disposition('attachment')

        message = Mail(
            from_email='abhishekyadav021004@gmail.com',
            to_emails=email,
            subject='Your MITS Internship Offer Letter',
            plain_text_content=f'Dear {name},\n\nPlease find attached your internship offer letter.\n\nThanks,\nMITS Team',
        )
        message.attachment = attachment
        sg.send(message)

        logging.info("Email sent successfully.")
        response = make_response("Offer letter emailed successfully.", 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        logging.error("An error occurred:")
        logging.error(traceback.format_exc())
        response = make_response(f"Internal Server Error: {str(e)}", 500)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
