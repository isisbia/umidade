# pyrefly: ignore [missing-import]
import firebase_admin
# pyrefly: ignore [missing-import]
import serial
# pyrefly: ignore [missing-import]
import threading
# pyrefly: ignore [missing-import]
import time
# pyrefly: ignore [missing-import]
import random

# pyrefly: ignore [missing-import]
from firebase_admin import credentials
# pyrefly: ignore [missing-import]
from firebase_admin import firestore
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, render_template_string

# Inicialização do Firebase
cred = credentials.Certificate("chaveapiisis.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# Configurações
PORTA_SERIAL = 'COM5' 
BAUD_RATE = 9600
INTERVALO_SALVAMENTO = 10  # Tempo em segundos

umidade_atual = 0.0

def salvar_no_firebase(valor_umidade):
    try:
        db.collection("leituras").add({
            "umidade": valor_umidade,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"Dados salvos no Firebase: Umidade = {valor_umidade}%")
    except Exception as e:
        print(f"Erro ao salvar no Firebase: {e}")

def loop_salvamento_firebase():
    print("Loop de salvamento no Firebase iniciado.")
    while True:
        time.sleep(INTERVALO_SALVAMENTO)
        # Só salva se já tiver alguma leitura real do Arduino
        if umidade_atual != 0.0:
            salvar_no_firebase(umidade_atual)

def ler_porta_serial():
    global umidade_atual
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
        print(f"Conectado ao Arduino na porta {PORTA_SERIAL}")
        
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode('utf-8')
                
                if "Umidade do Solo: " in linha:
                    try:
                        valor_str = linha.split("Umidade do Solo: ")[1].split('%')[0].strip()
                        umidade_atual = float(valor_str) 
                    except ValueError:
                        pass
    except Exception as e:
        print(f'Erro na comunicação Serial: {e}')
        print('Verifique se a porta está correta ou se o monitor serial da IDE não está aberto.')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Umidade do Solo</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background-color: #f4f4f9; padding-top: 100px; }
        .card { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #333; margin-top: 0;}
        .valor { font-size: 5em; font-weight: bold; color: #0078D7; }
        .unidade { font-size: 0.4em; color: #666; margin-left: 5px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Umidade Atual</h1>
        <div class="valor" id="umidade-display">--</div>
    </div>

    <script>
        function buscarUmidade() {
            fetch('/api/dados')
                .then(response => response.json())
                .then(data => {
                    // Atualiza o valor e adiciona o símbolo de %
                    document.getElementById('umidade-display').innerHTML = data.umidade.toFixed(0) + '<span class="unidade">%</span>';
                })
                .catch(error => console.error('Erro de conexão:', error));
        }

        setInterval(buscarUmidade, 500);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/dados')
def api_dados():
    return jsonify({"umidade": umidade_atual})

if __name__ == '__main__':
    # Thread 1: Cuida da leitura do Arduino (para não travar o Flask)
    thread_arduino = threading.Thread(target=ler_porta_serial, daemon=True)
    thread_arduino.start()

    # Thread 2: Cuida do envio para o Firebase a cada 10s
    thread_firebase = threading.Thread(target=loop_salvamento_firebase, daemon=True)
    thread_firebase.start()

    # Inicia o servidor Flask na porta 80
    print("Iniciando servidor web na porta 80...")
    app.run(host='0.0.0.0', port=80)