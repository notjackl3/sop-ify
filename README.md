# SOP-ify 📝
A simple Flask web app that compares two `.docx` files and highlights changes in content and formatting. Designed to help teams keep track of updates in SOPs, guides, and other documentation.

## 🚀 Features

- Upload and compare two Word documents
- Detect changes in text, additions, removals
- Detect formatting changes (e.g., bold text)
- Real-time update detection using a file watcher
- Clean, user-friendly web interface

## How It's Made:

**Tech used:** Python, Flask, HTML, CSS, JavaScript
The backend is powered by Flask. It handles file uploads, processes `.docx` files using Python’s `python-docx` library, and compares the documents for both content and styling differences (like bold or italic text). The app continuously watches for changes in the uploaded files using `watchdog`, allowing for live updates.

The frontend is built with basic HTML, CSS, and JavaScript. Users can upload two files, click a "Compare" button, and instantly see a list of changes. The page uses JavaScript polling to regularly check for changes in the background, providing a real-time comparison experience.

## Lessons Learned:

No matter what your experience level, being an engineer means continuously learning. Every time you build something you always have those *whoa this is awesome* or *wow I actually did it!* moments. This is where you should share those moments! Recruiters and interviewers love to see that you're self-aware and passionate about growing.

## 🛠 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/sop-ify.git
cd sop-ify
```

2. **Set up a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install the dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```


