'''
Install (Mac): pip3 install flask

Run (Mac): python3 stocks-webapp.py
'''

from flask import Flask, render_template,request
import collections

app = Flask(__name__)

# Used to render templates/index.html
@app.route('/',methods = ['GET'])

# Handles the data the user entered in the form.
@app.route('/send',methods = ['GET','POST'])
def send():
    if request.method == 'POST':
        csv = request.form['csv']
        correlation = compute_matrix(csv)
        return render_template('csv.html',csv=correlation)
    return render_template('index.html')

# Handles the file the user uploaded.
@app.route('/upload',methods = ['GET','POST'])
def upload_file():
   if request.method == 'POST':
      csvfile = request.files['file']
      textbytes = csvfile.read()
      text = textbytes.decode("utf-8")
      correlation = compute_matrix(text)
      return render_template('csv.html',csv=correlation)

# A and B are equal length arrays of stock prices.
def compute_correlation(A, B):
    num_dates = len(A)
    result = 0
    for i in range(1,num_dates):
        if (A[i] - A[i-1] < 0 and B[i] - B[i-1] < 0
            or A[i] - A[i-1] > 0 and B[i] - B[i-1] > 0
            or A[i] - A[i-1] == 0 and B[i] - B[i-1] == 0):
            result += 1
        else:
            result -= 1

    return result
            

def correlated_stocks(M, stocks):
    result = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] > 0:
                correlation_strength = float(M[i][j])/len(M)
                result.append({"s1":stocks[i], "s2":stocks[j], "corr":f"{correlation_strength:.2f}"})

    return result

        
def compute_matrix(csv):
    prices = collections.defaultdict(list)
    stocks = []
    # {"xom": [1,2,3], "ge", [3,4,5]}
    lines = csv.strip().split("\n")
    for line in lines:
        # line = "xom,1,2,3"
        parsed_line = line.split(",")
        symbol = parsed_line[0]
        stocks.append(symbol)
        # parsed_line = ["xom", "1", "2", "3"]
        for i in range(1,len(parsed_line)):
            prices[symbol].append(float(parsed_line[i]))

    result = [[0.0 for _ in range(len(stocks))] for _ in range(len(stocks))]
    for i in range(len(stocks)):
        for j in range(i+1,len(stocks)):
            corr = compute_correlation(prices[stocks[i]], prices[stocks[j]])
            result[i][j] = corr

    return correlated_stocks(result, stocks)


if __name__ == '__main__':
    app.run()
