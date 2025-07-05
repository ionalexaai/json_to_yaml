from flask_restful import Resource
from flask import request, make_response
import json

class JsonFormatter(Resource):

    def get(self):
        """Serve HTML form for manual JSON formatting"""
        html_form = """
        <html>
        <head>
            <title>JSON Formatter</title>
        </head>
        <body>
            <h2>JSON Formatter</h2>
            <form method="POST">
                <textarea name="json_data" rows="20" cols="80" placeholder="Enter raw JSON here..."></textarea><br><br>
                <input type="submit" value="Format JSON">
            </form>
        </body>
        </html>
        """
        response = make_response(html_form, 200)
        response.mimetype = "text/html"
        return response

    def post(self):
        """Format JSON from form or raw POST request"""
        try:
            json_data = request.form.get("json_data")

            if not json_data:
                # Fallback to raw body for API calls
                json_data = request.data.decode("utf-8")

            parsed = json.loads(json_data)
            formatted_json = json.dumps(parsed, indent=2)

            if request.form.get("json_data") is not None:
                # HTML with Copy to Clipboard button
                response_html = f"""
<html>
<head>
    <title>Formatted JSON</title>
    <!-- Prism.js CSS -->
    <link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.css" rel="stylesheet" />

    <style>
    pre {{
        background-color: #f4f4f4;
        padding: 10px;
        border: 1px solid #ddd;
        overflow-x: auto;
    }}
    button {{
        margin-top: 10px;
    }}
    </style>
</head>
<body>
    <h2>Formatted JSON</h2>
    <pre><code class="language-json" id="formatted_json">{formatted_json}</code></pre>

    <button onclick="copyToClipboard()">Copy to Clipboard</button>
    <br><br>
    <a href="">Back to form</a>

    <!-- Prism.js Library -->
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-json.min.js"></script>

    <script>
    function copyToClipboard() {{
        const text = document.getElementById('formatted_json').innerText;

        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(function() {{
                alert('Formatted JSON copied to clipboard!');
            }}).catch(function(err) {{
                alert('Failed to copy: ' + err);
            }});
        }} else {{
            const tempTextArea = document.createElement('textarea');
            tempTextArea.value = text;
            document.body.appendChild(tempTextArea);
            tempTextArea.select();
            try {{
                document.execCommand('copy');
                alert('Formatted JSON copied to clipboard!');
            }} catch (err) {{
                alert('Fallback copy failed: ' + err);
            }}
            document.body.removeChild(tempTextArea);
        }}
    }}
    </script>
</body>
</html>
"""

                response = make_response(response_html, 200)
                response.mimetype = "text/html"
                return response


            # API call response (JSON with proper mimetype)
            response = make_response(formatted_json, 200)
            response.mimetype = "application/json"
            return response

        except Exception as e:
            return {"error": str(e)}, 400
