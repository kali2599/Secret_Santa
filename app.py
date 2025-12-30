from flask import Flask, request, render_template, session
import random, os, json

app = Flask(__name__)
app.secret_key = "supersecretkey"


pairs = {"Chiara": 510, "Letizia": 957, "Federico": 655, "Davide": 0, "Ilaria": 654, "Silvia": 840, "Elena": 734}

codes = list(pairs.values())       # [510, 957, 655, 0, 654, 840, 734]
names = ["Davide", "Federico", "Silvia", "Chiara", "Elena", "Letizia", "Ilaria"]


        
def my_shuffle(codes, names, pairs):
    out = {}
    names_copy = names[:]
    for code in codes:
        admit = False
        while not admit:
            name = random.choice(names_copy)
            if code != pairs[name]:
                admit = True
                names_copy.remove(name)
                out[code] = name
    return out


#TODO: test if the file is effectively created only once for everyone
secret_santa = my_shuffle(codes, names, pairs)
if os.path.exists("secret_santa.json"):
    with open("secret_santa.json", "r") as file:
        secret_santa = json.load(file)
else:
    secret_santa = my_shuffle(codes, names, pairs)
    with open("secret_santa.json", "w") as file:
        json.dump(secret_santa, file)
    
print(secret_santa)
    

@app.route("/", methods=["GET", "POST"])
def index():

    #session.clear()

    if "attempts" not in session:
        session["attempts"] = 2

    #print(session)

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
