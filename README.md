# SOP-ify 📝📝
This lask web app that compares two `.docx` files and highlights changes in content and formatting. Designed to help user keep track of updates in SOPs, guides, and other documentation.

*(I had a documentation-focused internship opportunity during this time. Because of many difficulties I had in keeping track of the document versions and changes, I applied my programming skills to create more efficient systems. This reduces the time I need to manually search for changes.)*

## Features

- Upload and compare two Word documents
- Detect changes in text, additions, removals
- Detect formatting changes (e.g., bold, coloring, highlight)
- Real-time update detection using a file watcher

## How It's Made:

**Tech used:** Python, Flask, HTML, CSS, JavaScript.

The backend is powered by Flask. It handles file uploads, processes `.docx` files using Python’s `python-docx` library, and compares the documents for both content and styling differences. The app continuously watches for changes in the files using `watchdog`, allowing for live updates.

The frontend is built using HTML, CSS, and JavaScript. Users can upload two files, and instantly see a list of changes. The page uses polling techniques to regularly check for changes in the background, providing a real-time comparison experience.

## What I Learned Through This Project:

- Develop a Flask app (with a Django background)
- Polling and long polling technique
- Keep track of local file changes

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/notjackl3/sop-ify.git
cd sop-ify
```

2. **Set up a virtual environment**

```bash
-- MacOS -- 
python3 -m venv .venv
source .venv/bin/activate  
```

```bash
-- Windows -- 
python -m venv .venv
.venv\Scripts\activate
```

3. **Install the dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```


