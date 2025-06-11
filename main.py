
import functions_framework
from flask import request, make_response
from io import BytesIO
from reportlab.pdfgen import canvas

@functions_framework.http
def generate_offer_letter(request):
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    req_json = request.get_json(silent=True)
    if not req_json:
        return {"error": "Invalid request"}, 400

    name = req_json.get('name')
    college = req_json.get('college')
    domain = req_json.get('domain')

    if not all([name, college, domain]):
        return {"error": "Missing fields"}, 400

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
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=offer_letter_{name.lower().replace(" ", "_")}.pdf'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
