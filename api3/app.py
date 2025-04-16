from flask import Flask
import datetime

app = Flask(__name__)

# Renomeei a função para refletir o que ela faz
@app.route('/time')
def show_time(): # Renomeado de show_date
    # Obtemos a hora inicial apenas para o caso do JavaScript falhar
    now = datetime.datetime.now()
    current_time = now.strftime('%H:%M:%S')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API 3 - A Hora Certa</title>
        <style>
            body, html {{
                height: 100%; margin: 0; display: flex;
                justify-content: center; align-items: center;
                background-color: #e1f5fe; /* Outro fundo suave */
                font-family: sans-serif;
            }}
            /* Mantive a classe, mas o conteúdo será atualizado via JS */
            a.time-link {{
                font-size: 11em; color: #01579b;
                text-decoration: none;
            }}
            a.time-link:hover {{
                color: #00796b;
            }}
        </style>
    </head>
    <body>

        <a href="http://localhost:5001/date" class="time-link" id="clock-link">{current_time}</a>


        <script>
            // Eu defino uma função para atualizar a hora
            function updateClock() {{
                // Eu crio um objeto Date do JavaScript para obter a hora atual do cliente
                const now = new Date();
                // Eu formato a hora (adicionando zeros à esquerda se necessário)
                const hours = String(now.getHours()).padStart(2, '0');
                const minutes = String(now.getMinutes()).padStart(2, '0');
                const seconds = String(now.getSeconds()).padStart(2, '0');
                const currentTimeString = `${{hours}}:${{minutes}}:${{seconds}}`;

                // Eu encontro o elemento do link pelo seu ID
                const clockLinkElement = document.getElementById('clock-link');
                // Eu atualizo o texto dentro do link com a hora atual
                if (clockLinkElement) {{ // Verifico se o elemento foi encontrado
                    clockLinkElement.textContent = currentTimeString;
                }}
            }}

            // Eu chamo a função uma vez imediatamente para mostrar a hora certa logo ao carregar
            updateClock();

            // Eu configuro um intervalo para chamar a função updateClock a cada 1000ms (1 segundo)
            // 'setInterval' faz com que a função seja executada repetidamente.
            setInterval(updateClock, 1000);
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)