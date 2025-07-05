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
  <button onclick="copyJson()">Copy JSON</button><br><br>
  <a href="">Back to form</a>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/jquery-jsonview/1.2.3/jquery.jsonview.min.css" rel="stylesheet" />
  <style>
    #json-renderer {{ margin: 10px; font-family: monospace; }}
  </style>
</head>
<body>
  <h2>Formatted JSON Viewer</h2>
  <div id="json-renderer"></div>
  <button onclick="copyJson()">Copy JSON</button><br><br>
  <a href="">Back to form</a>

  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-jsonview/1.2.3/jquery.jsonview.min.js"></script>

  <script>
    const data = {escaped_json};
    $("#json-renderer").JSONView(data, {{
      collapsed: true,
      nl2br: false,
      recursive_collapser: true
    }});
    function copyJson() {{
      const txt = JSON.stringify(data, null, 2);
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(txt).then(() => alert("Copied!"));
      }} else {{
        const ta = document.createElement('textarea');
        ta.value = txt;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        alert("Copied!");
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
