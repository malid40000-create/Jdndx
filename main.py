from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-jwt-token', methods=['GET'])
def get_jwt_token():
    access_token = request.args.get('access_token')
    
    if not access_token:
        return jsonify({"error": "Access token required"}), 400
    
    # External API call
    url = f"https://jexar-access-token-to-jwt.vercel.app/api/get_jwt?access_token={access_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "token" in data:
            return jsonify({"token": data["token"]})
        else:
            return jsonify({"error": "JWT token not found in response", "raw_response": data}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to JWT service", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
