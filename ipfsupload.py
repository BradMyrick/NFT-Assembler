import flask
from flask import request
from flask_cors import CORS
import json
import requests
from werkzeug.utils import secure_filename
import urllib.request
from dotenv import dotenv_values


app = flask.Flask(__name__)
CORS(app)

ipfs_token = dotenv_values(".env")['IPFS_TOKEN']
ipfs_endpoint = 'https://api.nft.storage/upload'


@app.route("/ipfs_upload_file", methods=["POST"])
def ipfsUpload(_file):
    file = request.files['file']
    file.save(secure_filename(file.filename))
    with open(file.filename, 'rb') as f:
        r = requests.post(ipfs_endpoint, files={'file': f}, headers={'Authorization': 'Bearer ' + ipfs_token})
        print(r.text)
        return r.text


def get_filename(cid):
    header = {"Authorization": 'Bearer {}'.format(ipfs_token)}
    data = requests.get('https://api.nft.storage/'+cid, headers=header).content
    data = json.loads(data.decode('utf-8'))
    return data['value']['files'][0]['name']


@app.route("/ipfs_retrieve_file", methods=["POST"])
def retrieveAssetFromIPFS():
    data = request.get_json()
    cid = data["cid"]
    url = "https://ipfs.io/ipfs/"+str(cid)+"/"+get_filename(cid)
    filename = get_filename(cid)
    urllib.request.urlretrieve(url, filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
