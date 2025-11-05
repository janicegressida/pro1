from flask import Flask, request, render_template, redirect
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

connect_str = f"DefaultEndpointsProtocol=https;AccountName={os.getenv('AZURE_STORAGE_ACCOUNT')};AccountKey={os.getenv('AZURE_STORAGE_KEY')};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(os.getenv('AZURE_CONTAINER'))

@app.route("/")
def index():
    blobs = container_client.list_blobs()
    return render_template("index.html", blobs=blobs)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file, overwrite=True)
    return redirect("/")

@app.route("/download/<filename>")
def download(filename):
    blob_client = container_client.get_blob_client(filename)
    return redirect(blob_client.url)

@app.route("/delete/<filename>")
def delete(filename):
    blob_client = container_client.get_blob_client(filename)
    blob_client.delete_blob()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
