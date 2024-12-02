# create the flask app
from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.get("/") # base home.html, or base.html
def index_get():
    return render_template("base.html")

# route 2
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    print(text)
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)