from flask import Flask, render_template, request, redirect, url_for, flash
import re
from api.model_deployment import predict_price

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return redirect(url_for("house_price_input"))
    return render_template("home.html")

@app.route('/house_price_input', methods=["GET","POST"])
def house_price_input():
    if request.method == "POST":
        return redirect(url_for("submit"))
    return render_template('house_price_input.html')

@app.route('/submit', methods=["POST"])
def submit():
    try:
        # Handle the form data
        user_name = request.form['user_name']
        location = request.form['location']
        sqrft = request.form['sqrft']
        bhk_text = request.form['bhk']
        
        # Regular expression to find integers
        pattern = r'\b(\d+)\b'

        # Find matches
        matches = re.findall(pattern, bhk_text)

        # Convert matches to integers
        integers = [int(match) for match in matches]
        bhk = integers[0]
        noBathrooms = integers[1]

        # Predict price using the model
        predicted_price = predict_price(location, sqrft, noBathrooms, bhk)

        # Redirect to the index page with the results
        return redirect(url_for("index", user_name=user_name, location=location, sqrft=sqrft, bhk=bhk, noBathrooms=noBathrooms, predicted_price=predicted_price))

    except Exception as e:
        # If there's an error, flash a message and redirect back to the input page
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for("house_price_input"))

@app.route('/index', methods=["GET"])
def index():
    user_name = request.args.get('user_name')
    location = request.args.get('location')
    sqrft = request.args.get('sqrft')
    bhk = request.args.get('bhk')
    noBathrooms = request.args.get('noBathrooms')
    predicted_price = request.args.get('predicted_price')

    return render_template('index.html', user_name=user_name, location=location, sqrft=sqrft, bhk=bhk, noBathrooms=noBathrooms, predicted_price=predicted_price)

# if __name__ == '__main__':
#     app.run()

