from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
api_token = 'INSERT'

@cross_origin()
@app.route('/triggerEbay', methods=['POST'])
def trigger_ebay():
    # Your API token

    print('called')

    # # The URL you're sending the request to
    url = 'INSERT'

    # The headers for your request
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }

    # Extract data from the incoming request
    incoming_data = request.json
    keyword = incoming_data.get("keyword")
    count = incoming_data.get("count")

    # The data you're sending with your request
    data = json.dumps([
        {
            "keyword": keyword,
            "count": count
        }
    ])

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request was successful.")
        # Return the response content
        return jsonify(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        return jsonify({"error": "Request failed", "status_code": response.status_code, "response": response.text}), response.status_code


@cross_origin()
@app.route('/triggerAmazon', methods=['POST'])
def trigger_amazon():
    print('amazon called')
    # Extract details from the incoming request
    incoming_data = request.json
    product_url = incoming_data.get("url")

    # Validate required information
    if not all([api_token, product_url]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Prepare the headers and data for the POST request
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }

    data = json.dumps([{"url": product_url}])

    # Make the POST request
    response = requests.post('INSERT',
                             headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Request failed", "status_code": response.status_code, "response": response.text}), response.status_code


@cross_origin()
@app.route('/fetchDataset', methods=['POST'])
def fetch_dataset():
    """
    Fetches dataset from the given URL with the provided API token.

    Parameters:
    - api_token (str): The API token for authorization.

    Returns:
    - dict: The JSON response from the API.
    """
    incoming_data = request.json
    collection_id = incoming_data.get("collection_id")
    # The URL from which to fetch the dataset
    url = f"https://api.brightdata.com/dca/dataset?id={collection_id}"
    print(url)

    # The headers to include with the request
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    print(response)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response
        return jsonify(response.json())
    else:
        # Return an error message if something went wrong
        return {"error": f"Failed to fetch dataset, status code: {response.status_code}"}

if __name__ == '__main__':
    app.run(debug=True)
