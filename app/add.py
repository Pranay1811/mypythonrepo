from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/add", methods=["GET", "POST"])
def add():
    # Accept JSON or query params
    if request.is_json:
        data = request.get_json()
        a = data.get("a")
        b = data.get("b")
    else:
        a = request.args.get("a")
        b = request.args.get("b")

    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return jsonify({"error":"Provide numeric 'a' and 'b'"}), 400

    return jsonify({"result": a + b})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
