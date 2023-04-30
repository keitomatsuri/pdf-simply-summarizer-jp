import os
import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from pdf_simply_summarizer import PdfSimplySummarizer

app = Flask(__name__)
CORS(app)
load_dotenv()

UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'pdf'}

MODEL_NAME = os.environ.get('MODEL_NAME')
TEMPERATURE = float(os.environ.get('TEMPERATURE'))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH'))

# uploaded_filesフォルダが存在しなければ作成
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_timestamp_to_filename(filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}{ext}"


@app.route('/simply-summarize-pdf', methods=['POST'])
def simply_summarize_pdf():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'ファイルが送信されていません。'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'ファイルが選択されていません。'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = add_timestamp_to_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)

            pdf_simply_summrizer = PdfSimplySummarizer(llm)
            result = pdf_simply_summrizer.run(file_path)
        except Exception as e:
            print(e)
            return jsonify({'status': 'success', 'message': '要約に失敗しました。'}), 400
        finally:
            os.remove(file_path)

        print(result)
        return jsonify({'status': 'success', 'message': result}), 200

    else:
        return jsonify({'status': 'error', 'message': '許可されていないファイル形式です。'}), 400


@app.errorhandler(413)
def payload_too_large(error):
    return jsonify({'status': 'error', 'message': 'ファイルサイズが上限を超えています。'}), 413


if __name__ == '__main__':
    app.run(debug=True)
