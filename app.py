from flask import Flask, render_template, jsonify, request
import os
from main import compare_documents
import threading, time, os, webbrowser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
latest_changes = []

def scan_files():
    file1_path = os.path.join(UPLOAD_FOLDER, 'file1.docx')
    file2_path = os.path.join(UPLOAD_FOLDER, 'file2.docx')
    if os.path.exists(file1_path) and os.path.exists(file2_path):
        global latest_changes
        latest_changes = compare_documents(file1_path, file2_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/changes', methods=['POST'])
def changes():
    scan_files()
    return jsonify({"latest_changes": latest_changes})

@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')
    if file1 and file2:
        file1_path = os.path.join(UPLOAD_FOLDER, 'file1.docx')
        file2_path = os.path.join(UPLOAD_FOLDER, 'file2.docx')
        file1.save(file1_path) 
        file2.save(file2_path)
    return render_template('result.html', file_path=os.path.abspath(file2_path))

def watch_files():
    class ChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith('.docx'):
                scan_files()

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, UPLOAD_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5001')

if __name__ == '__main__':
    threading.Thread(target=watch_files, daemon=True).start()
    threading.Thread(target=open_browser).start()
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)