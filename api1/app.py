import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():

    api2_target_url = os.environ.get('API2_URL','http://localhost:5001/date')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API 1 - Primeira pergunta</title>
        <style>
            body, html {{
                height: 100%;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f0f0f0;
                font-family: sans-serif;
            }}
            a.link {{
                font-size: 9em;
                color: #333;
                text-decoration: none;
            }}
            a.link:hover {{
                color: #00796b;
            }}
        </style>
    </head>
    <body>
        <a href="{api2_target_url}" class="link">WHAT DAY IS TODAY?</a>
    </body>
    </html>
    """

    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
