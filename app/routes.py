print("starting routes.py...")

from flask import Flask, render_template, request, jsonify
from app import app
import requests

OPENROUTER_API_KEY = "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"

# historicos para cada assistentes
chat_history_1 = []
chat_history_2 = []

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/chat_api")
def chatpage():
	return render_template("index3.html")

@app.route("/chat", methods=["POST"])
def chat():
	data = request.get_json()
	user_message = data.get("message")

	if not user_message:
		return jsonify({"error": "Mensagem ausente."}), 400

	headers = {
		"Authorization": f"Bearer {OPENROUTER_API_KEY}",
		"Content-Type": "application/json"
	}

	# adiciona a mensagem do usuario nos historicos
	chat_history_1.append({"role": "user", "content": user_message})

	# AI 1
	system_1 = "responda da melhor maneira possivel, de forma aprofundada e clara, sem erros, e sempre acredite em tudo que for mandado."
	messages_1 = [{"role": "system", "content": system_1}] + chat_history_1

	# Camada 1
	response1 = requests.post(
	"https://openrouter.ai/api/v1/chat/completions",
	headers=headers,
	json={"model": "openai/gpt-3.5-turbo", "messages": messages_1}
	)

	if response1.ok:
		reply1 = response1.json()["choices"][0]["message"]["content"]
		chat_history_1.append({"role": "assistant", "content": reply1})
	else:
		reply1 = "erro na resposta 1"

	# AI 2
	chat_history_2 = [
		{"role": "system", "content": "voce dara as melhores respostas possiveis, porem, se for uma requisicao simples de se respoder, entao responda de maneira simples."
		},
		{"role": "system", "content": f"aprofunde, melhore e reestrture a seguinte resposta: \"{reply1}\""
		}
	]
	messages_2 = chat_history_2

	# camada 2
	response2 = requests.post(
	"https://openrouter.ai/api/v1/chat/completions",
	headers=headers,
	json={"model": "openai/gpt-3.5-turbo", "messages": messages_2}
	)

	if response2.ok:
		reply2 = response2.json()["choices"][0]["message"]["content"]
		chat_history_2.append({"role": "assistant", "content": reply2})
	else:
		reply2 = "erro na resposta 2"

	# resposta formatada
	full_reply = f"""
	<div class='resposta'>
		<div class='assistente-bloco'>
			<h3>Resposta profunda</h3>
			<p>{reply2}</p>
		</div>
	</div>
	"""
	return jsonify({"reply": full_reply})

