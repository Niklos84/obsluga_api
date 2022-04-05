import requests
import csv
from flask import Flask, render_template, request
app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

data_dict = data[0]
data_rates = (data_dict['rates'])
with open('rates.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(data_rates[0])
for i in data_rates:
    with open('rates.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, dialect='unix', quoting=csv.QUOTE_NONE)
        writer.writerow([i["currency"]+";"+i["code"]+";"+str(i["bid"])+";"+str(i["ask"])])

code_list = []
for i in data_rates:
    code_list.append(i["code"])

@app.route("/currency_calculator", methods=["GET", "POST"])
def calc():
    if request.method == "POST":
        data = request.form
        currency = data.get("currency")
        amount = float(data.get("amount"))
        result = 0
        for i in data_rates:
            if i["code"] == currency:
                result = i["ask"] * amount

    return render_template("currency_calculator.html", items=code_list, result=result)

if __name__ == "__main__":
    app.run(debug=True)