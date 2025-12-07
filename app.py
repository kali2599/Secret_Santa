import os
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render injects the correct port
    app.run(host="0.0.0.0", port=port)
