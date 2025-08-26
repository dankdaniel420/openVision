from flask import request, jsonify, Flask
import markdown
import codecs
import grokapi
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()