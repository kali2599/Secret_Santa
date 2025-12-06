from flask import Flask, request, render_template_string

app = Flask(__name__)

messages = {
    "Davide" : "",
    "Federico" : "",
    "Silvia" : "",
    "Chiara" : "",
    "Letizia" : "",
    "Ilaria" : "",
    "Elena" : ""
}

html = """
<h2>Enter your name</h2>
<form method="post">
  <input name="name">
  <button type="submit">Submit</button>
</form>

{% if message %}
<p>{{ message }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        name = request.form["name"]
        message = messages.get(name, "Name not found.")
    return render_template_string(html, message=message)

app.run(port=5000)
