````md
# 🌱 Monitor de Umidade do Solo com Arduino, Flask e Firebase

Sistema de monitoramento de umidade do solo utilizando **Arduino**, **Python**, **Flask** e **Firebase Firestore**, com atualização em tempo real via interface web.

O projeto realiza a leitura da umidade do solo através de um sensor conectado ao Arduino, exibe os dados em uma interface web e armazena as leituras automaticamente no Firebase.

---

## 📌 Funcionalidades

✅ Leitura de dados do sensor de umidade via porta serial (Arduino)

✅ Exibição em tempo real da umidade do solo

✅ Interface web simples e responsiva

✅ Salvamento automático das leituras no Firebase Firestore

✅ Atualização contínua dos dados sem precisar recarregar a página

---

## 🛠️ Tecnologias Utilizadas

- Python
- Flask
- Firebase Firestore
- Arduino
- PySerial
- HTML, CSS e JavaScript

---

## 📂 Estrutura do Projeto

```bash
📦 projeto-umidade
├── app.py                  # Aplicação principal Flask
├── chaveapiisis.json       # Credenciais do Firebase
├── dev_iot/                # Ambiente/projeto relacionado ao IoT
└── .venv/                  # Ambiente virtual Python
````

---

## ⚙️ Como Funciona

1. O **Arduino** coleta os dados do sensor de umidade do solo.
2. Os dados são enviados pela **porta serial (COM)**.
3. O **Python** lê essas informações continuamente.
4. O sistema atualiza a interface web em tempo real.
5. A cada **10 segundos**, os dados são enviados para o **Firebase Firestore**.

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/isisbia/umidade
```

Entre na pasta do projeto:

```bash
cd umidade
```

---

### 2. Crie um ambiente virtual (opcional)

```bash
python -m venv .venv
```

Ative o ambiente virtual:

### Windows

```bash
.venv\Scripts\activate
```

### Linux/Mac

```bash
source .venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install flask firebase-admin pyserial
```

---

### 4. Configure o Firebase

1. Acesse o console do Firebase
2. Crie um projeto
3. Vá em:

```text
Configurações do projeto → Contas de serviço
```

4. Gere uma chave privada JSON
5. Salve o arquivo no projeto com o nome:

```text
chaveapiisis.json
```

---

### 5. Configure a Porta Serial

No arquivo `app.py`, altere a porta do Arduino caso necessário:

```python
PORTA_SERIAL = 'COM5'
```

Exemplos:

* `COM3`
* `COM4`
* `COM5`

Você pode verificar a porta no **Gerenciador de Dispositivos do Windows**.

---

### 6. Execute a aplicação

```bash
python app.py
```

O sistema iniciará o servidor Flask.

---

## 📊 Exemplo de Dados Salvos no Firebase

```json
{
  "umidade": 62.4,
  "timestamp": "2026-06-12T10:00:00"
}
```

---

## 📸 Interface

A aplicação exibe:

* Umidade atual do solo (%)
* Atualização automática em tempo real
* Layout simples e intuitivo

---

## 👨‍💻 Projeto acadêmico/IoT para monitoramento inteligente da umidade do solo - DSM/4° Semestre - Fatec Matão.
