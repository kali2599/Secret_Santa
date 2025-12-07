from flask import Flask, request, render_template, session
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

pairs = {"Sasso": 510, "Letizia" : 957, "Feffo": 655, "Davide": 0, "Ilaria": 654, "Silvia": 840, "Elena": 734}

# ---- SECRET SANTA SETUP ----
codes = [510, 957, 655, 654, 840, 734, 0]
names = ["Davide","Federico","Silvia","Chiara","Elena","Letizia","Ilaria"]

random.shuffle(names)
secret_santa = dict(zip(codes, names))

@app.route("/", methods=["GET", "POST"])
def index():

    #session.clear()

    if "attempts" not in session:
        session["attempts"] = 2

    print(session)

    message = ""
    santa_name = ""
    correct = False
    attempts_left = session["attempts"]

    if attempts_left <= 0:
        return render_template(
            "index.html",
            attempts_left=0,
            message="❌ No attempts left. Access denied.",
            correct=False,
            santa_name=""
        )

    if request.method == "POST":
        code_str = request.form.get("code", "")

        if not code_str.isdigit():
            session["attempts"] -= 1
            return render_template(
                "index.html",
                attempts_left=session["attempts"],
                message="⚠️ Code must be a number!",
                correct=False,
                santa_name=""
            )

        code = int(code_str)

        if code in secret_santa:
            santa_name = secret_santa[code]
            correct = True
            message = ""
        else:
            session["attempts"] -= 1
            message = "❌ Wrong code! Try again."

        attempts_left = session["attempts"]

    return render_template(
        "index.html",
        attempts_left=attempts_left,
        message=message,
        correct=correct,
        santa_name=santa_name
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render injects the correct port
    app.run(host="0.0.0.0", port=port)
