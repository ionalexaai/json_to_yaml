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
                    <script>
                    function copyToClipboard() {{
                        const text = document.getElementById('formatted_json').innerText;
                        navigator.clipboard.writeText(text).then(function() {{
                            alert('Formatted JSON copied to clipboard!');
                        }}, function(err) {{
                            alert('Failed to copy: ' + err);
                        }});
                    }}
                    </script>
                </head>
                <body>
                    <h2>Formatted JSON</h2>
                    <a href="">Back to form</a>
                    <button onclick="copyToClipboard()">Copy to Clipboard</button>
                    <pre><code id="formatted_json">{formatted_json}</code></pre>
                    <button onclick="copyToClipboard()">Copy to Clipboard</button>
                    <br><br>
                    <a href="">Back to form</a>
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
