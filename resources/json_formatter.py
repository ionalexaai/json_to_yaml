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
                json_data = request.data.decode("utf-8")

            parsed = json.loads(json_data)
            formatted_json = json.dumps(parsed, indent=2)
            escaped_json = json.dumps(parsed)  # Compact version for JS embedding

            response_html = f"""
            <html>
            <head>
                <title>Formatted JSON (Collapsible)</title>
                <link href="https://cdn.jsdelivr.net/npm/json-viewer-js@latest/dist/json-viewer.min.css" rel="stylesheet">
                <style>
                    #json-renderer {{
                        font-family: Consolas, monospace;
                        background-color: #f4f4f4;
                        padding: 10px;
                        border: 1px solid #ddd;
                        overflow-x: auto;
                    }}
                </style>
            </head>
            <body>
                <h2>Formatted JSON (Collapsible Viewer)</h2>
                <div id="json-renderer"></div>
                <button onclick="copyToClipboard()">Copy to Clipboard</button>
                <br><br>
                <a href="">Back to form</a>

                <script src="https://cdn.jsdelivr.net/npm/json-viewer-js@latest/dist/json-viewer.min.js"></script>

                <script>
                    const jsonData = {escaped_json};

                    const viewer = new JSONViewer();
                    document.getElementById("json-renderer").appendChild(viewer.getContainer());
                    viewer.showJSON(jsonData, 1, 1);  // Collapse level 1 by default

                    function copyToClipboard() {{
                        const text = JSON.stringify(jsonData, null, 2);
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
                                alert('Copied!');
                            }} catch (err) {{
                                alert('Copy failed: ' + err);
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
