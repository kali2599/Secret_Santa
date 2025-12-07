from flask import Flask, request, render_template_string, session
import random, os

app = Flask(__name__)
app.secret_key = "supersecretkey"   # required for session

# ---- SECRET SANTA SETUP ----
codes = [0,1,2,3,4,5,6]
names = ["Davide","Federico","Silvia","Chiara","Elena","Letizia","Ilaria"]

random.shuffle(names)
secret_santa = dict(zip(codes, names))

# ---- HTML TEMPLATE ----
html = """
<h2>Enter your code</h2>

{% if attempts_left is not none %}
<p><strong>Attempts remaining:</strong> {{ attempts_left }}</p>
{% endif %}

<form method="post">
  <input name="code" placeholder="Enter code">
  <button type="submit">Submit</button>
</form>

{% if message %}
<p><strong>{{ message }}</strong></p>
{% endif %}
"""

# ---- ROUTE ----
@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize attempts if not present
    if "attempts" not in session:
        session["attempts"] = 3   # user gets 3 attempts total

    message = ""
    attempts_left = session["attempts"]

    # Stop if attempts exhausted
    if attempts_left <= 0:
        return render_template_string(
            html,
            message="No attempts left. Access denied.",
            attempts_left=0
        )

    if request.method == "POST":
        code_str = request.form["code"]

        # Ensure the input is numeric
        if not code_str.isdigit():
            session["attempts"] -= 1
            return render_template_string(
                html,
                message="Code must be a number.",
                attempts_left=session["attempts"]
            )

        code = int(code_str)

        # Check if code exists
        if code in secret_santa:
            assigned = secret_santa[code]
            message = f"Your Secret Santa is: {assigned}"
        else:
            session["attempts"] -= 1
            message = f"Wrong code! Try again."

        attempts_left = session["attempts"]

    return render_template_string(html, message=message, attempts_left=attempts_left)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render injects the correct port
    app.run(host="0.0.0.0", port=port)
