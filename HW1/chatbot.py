from flask import Flask, render_template, request

app = Flask(__name__)

# Define a dictionary of responses
responses = {
    "hi": "Hello!",
    "how are you?": "I'm fine, thank you!",
    "bye": "Goodbye!",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["user_message"].lower()
    bot_reply = responses.get(user_message, "Sorry, I don't understand that.")
    return render_template("index.html", user_message=user_message, bot_reply=bot_reply)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
