from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import yagmail
import os

app = Flask(__name__)

# Allow cross-origin requests from your deployed Vercel frontend
CORS(app, resources={r"/*": {"origins": "https://frontend-661k.vercel.app"}}, supports_credentials=True)

# Replace with your actual credentials
SENDER_EMAIL = "sarahssamplingsetup@gmail.com"
APP_PASSWORD = "isbmdzlumghhpgig"

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    samples = data['samples']
    location = data['location'].replace(" ", "_")
    recipient_email = data['email']

    # Create Excel file
    df = pd.DataFrame(samples)
    filename = f"{location}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(os.getcwd(), filename)
    df.to_excel(filepath, index=False)

    # Send email with attachment
    try:
        print(f"📤 Sending email to: {recipient_email}")
        yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
        subject = f"Water Quality Data - {location}"
        body = f"Attached is the Excel file for your sampling location: {location}."
        yag.send(to=recipient_email, subject=subject, contents=body, attachments=filepath)
        print("✅ Email sent successfully!")
        return jsonify({"message": "Excel file created and emailed successfully!"})
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

