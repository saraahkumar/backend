from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
import traceback

app = Flask(__name__)

# Allow cross-origin requests from your deployed Vercel frontend
CORS(app, resources={r"/*": {"origins": "https://frontend-661k.vercel.app"}}, supports_credentials=True)

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        samples = data['samples']
        location = data['location'].replace(" ", "_")

        # Create Excel file
        df = pd.DataFrame(samples)
        filename = f"{location}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join("/tmp", filename)  # Use /tmp for Render safety

        df.to_excel(filepath, index=False)
        print(f"✅ File created at {filepath}, sending as download.")

        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        print(f"❌ Failed to send file: {e}")
        traceback.print_exc()
        return jsonify({"message": f"Failed to send file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

