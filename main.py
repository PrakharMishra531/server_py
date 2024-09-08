from flask import Flask, request, send_file
import os
import extractor

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.exists(UPLOAD_FOLDER):
    shutil.rmtree(UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER)

if os.path.exists('section.pdf'):
    os.remove('section.pdf')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith('.zip'):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        try:
            extractor.extract_data()
        except Exception as e:
            return f'Error while extracting data: {str(e)}', 500
        try:
            import get_info
            message = get_info.feed_ai()
            get_info.get_info(message)
        except Exception as e:
            return f'Error while processing info: {str(e)}', 500
        return 'File uploaded successfully', 200
    return 'Invalid file type', 400

@app.route('/download', methods=['GET'])
def download_file():
    filename = 'section.pdf'
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

    
