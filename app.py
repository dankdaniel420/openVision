from flask import request, jsonify, Flask
from waitress import serve
import markdown
import codecs
import grokapi
import excel_zip
import logging

app = Flask(__name__)

@app.route("/")
def index():
    """Parses README.md and displays it as HTML."""
    # Read README.md, convert to HTML
    input_file = codecs.open("README.md", mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)

    # Add CSS for styling
    styled_html = f"""
    <style>
        body {{
            font-family: sans-serif;
            margin: 0;
            padding: 2em;
        }}
        .content {{
            max-width: 70%;
            margin: 0 auto;
        }}
    </style>
    <div class="content">
        {html}
    </div>
    """
    return styled_html

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    base64_image = data.get("image")
    query_text = data.get("query")
    logging.info(f"Received query: {query_text}")
    response = grokapi.query_image(base64_image, query_text)
    return jsonify(response)

# zip csv content and return base64 zip
@app.route("/content", methods=["POST"])
def store_content():
    req = request.get_json()
    file_name = req.get("fileName", "IFRS_Validation_Report.xlsx")
    content_string = req.get("contentString")
    zip = excel_zip.compress(file_name, content_string)
    return jsonify({"base64_zip": zip})

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(app, host="0.0.0.0", port=5000)