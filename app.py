from flask import Flask, request, render_template, session
import random, os, json

app = Flask(__name__)
app.secret_key = "supersecretkey"


pairs = {"Sasso": 510, "Letizia": 957, "Feffo": 655, "Davide": 0, "Ilaria": 654, "Silvia": 840, "Elena": 734}

codes = list(pairs.values())       # [510, 957, 655, 0, 654, 840, 734]
names = ["Davide", "Federico", "Silvia", "Chiara", "Elena", "Letizia", "Ilaria"]

def deranged_shuffle(codes, names, pairs):
    """Shuffle names so that no code gets its original name in pairs"""
    while True:
        shuffled = names[:]
        random.shuffle(shuffled)
        # check for conflicts with pairs
        conflict = False
        for name, code in pairs.items():
            if shuffled[codes.index(code)] == name:
                conflict = True
                break
        if not conflict:
            return dict(zip(codes, shuffled))

secret_santa = deranged_shuffle(codes, names, pairs)

with open("secret_santa.json", "w") as file:
    json.dump(secret_santa, file)
    

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
            with open("secret_santa.json") as f:
                secret_santa_file = json.load(f)
                santa_name = secret_santa_file[str(code)]
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
