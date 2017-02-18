from flask import Flask, jsonify, request
import cloudsight
import httplib, urllib, base64, json

app = Flask(__name__)

auth = cloudsight.SimpleAuth('kZH5jI5q2CSUD5Ofrsd8Dg')
api = cloudsight.API(auth)

MS_VISION_KEY = '6c8fa85edf7c47488eae0f1a6827b72c'

@app.route('/cloudsight/v1.0/image/',methods=['GET'])
def index():
	url = request.args.get('url')
	response = api.remote_image_request(url, {
     'image_request[locale]': 'en-US',
	})
	status = api.wait(response['token'], timeout=30)
	return jsonify(status)

@app.route('/ms/describe/', methods=['GET'])
def describe_image():
	url = request.args.get('url')
	headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': MS_VISION_KEY,
	}

	params = urllib.urlencode({
	    # Request parameters
	    'maxCandidates': '1',
	})

	body = "{'Url':'" + url + "'}"

	
	conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	conn.request("POST", "/vision/v1.0/describe?%s" % params, body, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
		

	return data

if __name__ == '__main__':
    app.run(debug=True)