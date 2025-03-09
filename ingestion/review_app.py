from flask import Flask, render_template_string, request, redirect, url_for, flash
import os, json
from ingestion.process_files import process_all_files

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
METADATA_FILE = os.path.join(UPLOAD_FOLDER, "metadata.json")

# Ensure necessary directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load or initialize metadata (to store file descriptions)
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
else:
    metadata = {}

# Common navigation menu used in all pages
NAV_HTML = """
<ul>
  <li><a href="{{ url_for('index') }}">Dashboard</a></li>
  <li><a href="{{ url_for('upload_file') }}">Upload Files</a></li>
  <li><a href="{{ url_for('process_files_route') }}">Process Files</a></li>
  <li><a href="{{ url_for('review_files') }}">Review Processed Files</a></li>
  <li><a href="{{ url_for('integration_info') }}">Integrate AI Agent</a></li>
</ul>
"""

INDEX_HTML = """
<!doctype html>
<title>AI Agent Dashboard</title>
<h1>AI Agent Dashboard</h1>
""" + NAV_HTML + """
<p>Welcome! Use the navigation links above to upload files, process them, review the results, or see integration instructions.</p>
"""

UPLOAD_HTML = """
<!doctype html>
<title>Upload File</title>
<h1>Upload a File</h1>
""" + NAV_HTML + """
<form method="post" enctype="multipart/form-data">
  <p>
    <label for="file">Select File:</label>
    <input type="file" name="file" required>
  </p>
  <p>
    <label for="description">File Description:</label>
    <input type="text" name="description" placeholder="Enter a description for the file">
  </p>
  <input type="submit" value="Upload">
</form>
"""

REVIEW_HTML = """
<!doctype html>
<title>Processed Files Review</title>
<h1>Processed Files</h1>
""" + NAV_HTML + """
<ul>
{% for file in files %}
  <li><a href="{{ url_for('view_file', filename=file) }}">{{ file }}</a></li>
{% endfor %}
</ul>
"""

VIEW_HTML = """
<!doctype html>
<title>Review {{ filename }}</title>
<h1>{{ filename }}</h1>
<pre>{{ content }}</pre>
<a href="{{ url_for('review_files') }}">Back to Review List</a>
"""

INTEGRATION_HTML = """
<!doctype html>
<title>Integrate AI Agent</title>
<h1>Integrate AI Agent</h1>
""" + NAV_HTML + """
<p>You can integrate your AI agent into various platforms:</p>
<ul>
  <li><strong>Website Integration:</strong> Embed the Rasa chat widget by adding a JavaScript snippet to your website.</li>
  <li><strong>Social Media Integration:</strong> Use platforms like Telegram (already configured), Facebook Messenger, or WhatsApp by setting up the appropriate webhooks and connectors.</li>
</ul>
<p>For website integration, for example, you could add the following snippet to your website's HTML:</p>
<pre>
&lt;script src="https://your-domain.com/path/to/chat-widget.js"&gt;&lt;/script&gt;
</pre>
<p>Consult the documentation for each platform for further details.</p>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    global metadata
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)
        description = request.form.get("description", "")
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # Save the description in metadata
        metadata[file.filename] = {"description": description}
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        flash("File uploaded successfully", "success")
        return redirect(url_for("index"))
    return render_template_string(UPLOAD_HTML)

@app.route("/process")
def process_files_route():
    process_all_files()
    flash("File processing complete", "success")
    return redirect(url_for("review_files"))

@app.route("/review")
def review_files():
    files = os.listdir(PROCESSED_FOLDER)
    return render_template_string(REVIEW_HTML, files=files)

@app.route("/view/<filename>")
def view_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return render_template_string(VIEW_HTML, filename=filename, content=content)

@app.route("/integrate")
def integration_info():
    return render_template_string(INTEGRATION_HTML)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
