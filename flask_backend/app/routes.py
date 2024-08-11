from flask import Blueprint, request, jsonify
import os
import random
import string
from app.utils.summarize import summarize_document,stop_summarization_process
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor

from flask_cors import CORS

bp = Blueprint('routes', __name__)
executor = ThreadPoolExecutor()

CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    name, ext = os.path.splitext(filename)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{name}_{random_string}{ext}"

def read_file_content(filepath):
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    elif ext == '.docx':
        import docx
        document = docx.Document(filepath)
        content = "\n".join([para.text for para in document.paragraphs])
    elif ext == '.pdf':
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
    else:
        content = None

    return content

# @bp.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     return response

@bp.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if request.method == "OPTIONS":
        return jsonify({}), 200
    elif request.method == "POST":
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                filename = generate_unique_filename(filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            content = read_file_content(filepath)
            if content is None:
                return jsonify({'error': 'File could not be read'}), 500

            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'content': content,
            }), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/summarize', methods=['POST', 'OPTIONS'])
def summarize():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    elif request.method == "POST":
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        executor.submit(summarize_document, filepath)
        return jsonify({'message': 'Summarization started'}), 202

@bp.route('/summarize/status', methods=['GET'])
def get_summarization_status():
    from app.utils.summarize import summarization_status
    return jsonify(summarization_status), 200

@bp.route('/stop', methods=['POST'])
def stop_summarization():
    summary = stop_summarization_process()
    return jsonify({"summary": summary})