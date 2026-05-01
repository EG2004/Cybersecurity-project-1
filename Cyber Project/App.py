from flask import Flask, render_template, request
from detector import rule_based_detection
from ml_model import ml_detection
import time

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    rule_result = ""
    ml_result = ""
    rule_time = ""
    ml_time = ""

    if request.method == "POST":
        user_input = request.form["user_input"]

        # Rule-based timing
        start = time.perf_counter()
        rule_result = rule_based_detection(user_input)
        rule_time = time.perf_counter() - start

        # ML timing
        start = time.perf_counter()
        ml_result = ml_detection(user_input)
        ml_time = time.perf_counter() - start

        # Convert to milliseconds (cleaner for display)
        rule_time = round(rule_time * 1000, 4)
        ml_time = round(ml_time * 1000, 4)

    return render_template(
        "index.html",
        user_input=user_input,
        rule_result=rule_result,
        ml_result=ml_result,
        rule_time=rule_time,
        ml_time=ml_time
    )


if __name__ == "__main__":
    app.run(debug=True)