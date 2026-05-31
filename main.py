from flask import Flask, request, make_response
import requests
import json
from datetime import datetime

app = Flask(__name__)

# మీ గూగుల్ వెబ్ యాప్ URL (ఇందాకటి కొత్త లింక్)
GOOGLE_WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbwUxATYX5F8P7ey_ZvWNZaT0emIvrNT80W9aVfJZxo_If8kkBoDnkX87tKnZhpvuzPLxg/exec'

@app.route('/iclock/cdata', methods=['GET', 'POST'])
def adms_server():
    # 1. మిషన్ మొదట కనెక్ట్ అయినప్పుడు అడిగే రిక్వెస్ట్ (Initialization)
    if request.method == 'GET' and request.args.get('type') == 'init':
        response = make_response("Server=OK\n")
        response.headers['Content-Type'] = 'text/plain'
        return response

    # 2. మిషన్ నుండి అటెండెన్స్ డేటా వచ్చినప్పుడు (POST Request)
    if request.method == 'POST':
        raw_data = request.get_data(as_text=True)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # ఇక్కడ మిషన్ డేటాను ముక్కలు చేసి ఎంప్లాయ్ ఐడీని వెతుకుతాం
        lines = raw_data.split('\n')
        for line in lines:
            if line.strip():
                parts = line.split('\t') # ADMS డేటా సాధారణంగా ట్యాబ్‌లతో ఉంటుంది
                if len(parts) >= 2:
                    emp_id = parts[0]
                    # డేటాను గూగుల్ షీట్‌కు పంపడం
                    payload = {
                        "user_id": emp_id,
                        "timestamp": current_time,
                        "status": "ADMS Cloud Live"
                    }
                    try:
                        requests.post(GOOGLE_WEBAPP_URL, data=json.dumps(payload))
                    except Exception as e:
                        print("Error sending to Sheets:", e)

        response = make_response("OK\n")
        response.headers['Content-Type'] = 'text/plain'
        return response

    # మిగతా సాధారణ రిక్వెస్ట్‌ల కోసం
    response = make_response("OK\n")
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
