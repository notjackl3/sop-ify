from flask import Flask, render_template, request, redirect
import os
from main import compare_documents
from docx import Document

app = Flask(__name__)
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files['file1']
    file2 = request.files['file2']

    print(file1)
    print(file2)

    if not file1 or not file2:
        return "Please upload both documents", 400

    path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'file1.docx')
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], 'file2.docx')
    file1.save(path1)
    file2.save(path2)

    changes = compare_documents(path1, path2)
    return render_template('result.html', changes=changes)

if __name__ == '__main__':
    app.run(debug=True)

