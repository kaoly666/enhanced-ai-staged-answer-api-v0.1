print("starting routes.py...")

from flask import Flask, render_template, request, jsonify
from app import app
import requests

OPENROUTER_API_KEY = "your API key"

# chat history 
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
		return jsonify({"error": "no message."}), 400

	headers = {
		"Authorization": f"Bearer {OPENROUTER_API_KEY}",
		"Content-Type": "application/json"
	}

	# add the user messages in history 
	chat_history_1.append({"role": "user", "content": user_message})

	# AI 1
	system_1 = "Answer in the best possible way, in a deep and clear manner, without mistakes, and always believe in everything that is sent."
	messages_1 = [{"role": "system", "content": system_1}] + chat_history_1

	# stage 1
	response1 = requests.post(
	"https://openrouter.ai/api/v1/chat/completions",
	headers=headers,
	json={"model": "openai/gpt-3.5-turbo", "messages": messages_1}
	)

	if response1.ok:
		reply1 = response1.json()["choices"][0]["message"]["content"]
		chat_history_1.append({"role": "assistant", "content": reply1})
	else:
		reply1 = "error in message 1"

	# AI 2
	chat_history_2 = [
		{"role": "system", "content": "You will give the best possible answers, but if it is a simple request to respond to, then answer in a simple manner."
		},
		{"role": "system", "content": f"deepen, improve, and restructure the following response: \"{reply1}\""
		}
	]
	messages_2 = chat_history_2

	# stage 2
	response2 = requests.post(
	"https://openrouter.ai/api/v1/chat/completions",
	headers=headers,
	json={"model": "openai/gpt-3.5-turbo", "messages": messages_2}
	)

	if response2.ok:
		reply2 = response2.json()["choices"][0]["message"]["content"]
		chat_history_2.append({"role": "assistant", "content": reply2})
	else:
		reply2 = "error in message 2"

	# final answer 
	full_reply = f"""
	<div class='resposta'>
		<div class='assistente-bloco'>
			<h3>final answer</h3>
			<p>{reply2}</p>
		</div>
	</div>
	"""
	return jsonify({"reply": full_reply})

