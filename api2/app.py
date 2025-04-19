import os
from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/date')
def show_date():
    today = datetime.date.today()
    current_date = today.strftime('%Y-%m-%d') # Formato AAAA-MM-DD

    #variavel ambiente para navecação entre apis
    api1_target_url = os.environ.get('API1_URL','http://localhost:5000')
    api3_target_url = os.environ.get('API3_URL','http://localhost:5002/time')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API 2 - A Data Certa</title>
        <style>
            body, html {{
                height: 100%; margin: 0; display: flex;
                /* Eu ajusto o flexbox para alinhar itens verticalmente */
                flex-direction: column; /* Faz os itens ficarem um abaixo do outro */
                justify-content: center; align-items: center;
                background-color: #f0f0f0; font-family: sans-serif;
                text-align: center; /* Garante que o texto dentro dos links fica centrado */
            }}
            /* Eu defino estilos para o link da data (grande) */
            a.date-link {{
                font-size: 11em; /* Mantém este grande */
                color: #333;
                text-decoration: none;
                display: block; /* Faz o link ocupar a linha inteira */
                margin-bottom: 20px; /* Adiciona um espaço abaixo da data */
            }}
            a.date-link:hover {{
                color: #00796b;
            }}
            /* Eu defino estilos para o link do desafio (mais pequeno) */
            a.challenge-link {{
                font-size: 3em; /* Tamanho significativamente menor */
                color: #555;
                text-decoration: none;
                display: block; /* Também ocupa a linha inteira */
            }}
            a.challenge-link:hover {{
                color: #0056b3; /* Cor diferente no hover */
            }}
        </style>
    </head>
    <body>
        <a href="{api1_target_url}" class="date-link">{current_date}</a>

        <a href="{api3_target_url}" class="challenge-link">I challenge you to tell me the time</a>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)