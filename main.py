import requests
import csv
from flask import Flask, render_template, request



response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
my_data = [] 

# wyodrebnienie potrzebnych wartosci do pustej listy
for _ in data[0]['rates']:
    x = [_['currency'], _['code'], _['bid'], _['ask']]
    my_data.append(x)

# zapis pliku csv
with open('currency.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows(my_data)


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = ''
    if request.method == "POST":
        currency = request.form.get('currency')
        quantity = request.form.get('ilosc')
        for i in my_data:
            if i[1] == currency:
                result = round(float(i[3]) * int(quantity),2)

    return render_template("web_calc.html", my_data=my_data, result=result)


if __name__=="__main__":
    app.run(debug=True)