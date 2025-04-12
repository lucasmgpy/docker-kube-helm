from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/date')
def show_date():
    today = datetime.date.today()
    current_date = today.strftime('%Y-%m-%d')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API 2 - A Data Certa</title>
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
            a.date-link {{
                font-size: 11em;
                color: #333;
                text-decoration: none;
            }}
            a.date-link:hover {{
                color: #00796b;
            }}
        </style>
    </head>
    <body>
        <a href="http://localhost:5000/" class="date-link">{current_date}</a>
        
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)