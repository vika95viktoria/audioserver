from flask import Flask, render_template, request, send_file
from audio_converter import convert_to_wav
from bucket_service import upload_to_bucket, delete_file
from google_tr import transcribe_gcs
from docx_server import create_word_doc
from werkzeug.exceptions import HTTPException
from file_manager import list_all_files_with_ext, delete_file_from_disk, delete_files
import yaml
import logging

app = Flask(__name__)

with open("config.yml", 'r') as yml_file:
    cfg = yaml.safe_load(yml_file)


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(e)
    if isinstance(e, HTTPException):
        return e
    return render_template("500_generic.html", e=e), 500


@app.route('/')
def index():
    old_transcripts = list_all_files_with_ext(".docx")
    old_transcripts.reverse()
    return render_template('index.html', files=old_transcripts)


@app.route('/uploader', methods=['GET', 'POST'])
def save_file_and_upload_file_to_bucket():
    old_wav_files = list_all_files_with_ext(".wav")
    old_mp3_files = list_all_files_with_ext(".mp3")
    old_transcripts = list_all_files_with_ext(".docx")
    delete_files(old_wav_files)
    delete_files(old_mp3_files)
    if len(old_transcripts) > 5:
        old_to_delete = old_transcripts[:-5]
        delete_files(old_to_delete)
    if request.method == 'POST':
        f = request.files['file']
        file_name = f.filename
        if not file_name.endswith(".mp3"):
            return render_template('400_error.html', error="Некорректный файл. Загрузите аудио в формате mp3, пожалуйста")
        f.save(file_name)
        logging.info(f"save file {file_name}")
        wav_file_name = file_name.split(".")[0]
        num_of_channels = convert_to_wav(f.filename, wav_file_name)
        wav_with_ext = wav_file_name + ".wav"
        bucket_name = cfg["bucket_name"]
        file_url = upload_to_bucket(wav_with_ext, wav_with_ext, bucket_name)
        logging.info(f"uploaded to bucket {file_url} channels {num_of_channels}")
        text = transcribe_gcs(file_url, num_of_channels, cfg["language"])
        path = create_word_doc(text, wav_file_name)
        delete_file(bucket_name, wav_with_ext)
        return render_template('index.html', filepath=path)


@app.route('/file/<path:filename>', methods=['GET', 'POST', 'DELETE'])
def download(filename):
    if request.method == 'DELETE':
        delete_file_from_disk(filename)
        return ""
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
