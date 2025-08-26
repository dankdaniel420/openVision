from flask import request, jsonify, Flask
import markdown
import codecs
import grokapi
import base64

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
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    query_text = request.form.get('query')

    if not query_text:
        return jsonify({"error": "No query text provided"}), 400

    # Read the image file's bytes and encode to base64
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    response = grokapi.query_image(base64_image, query_text)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)