# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Classifier model
filename = r'C:\Users\DELL\Desktop\ML\Datasets\INeuron ML challenge\Back order prediction\backorder_prediction_model.pkl'
classifier = pickle.load(open(filename, 'rb'))

app = Flask(__name__, static_url_path='', 
            static_folder=r'C:\Users\DELL\Desktop\ML\Datasets\INeuron ML challenge\Back order prediction\static',)

@app.route('/')
def home():
    return render_template(r'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        national_inv = int(request.form['National Inventory'])
        lead_time = int(request.form['Lead Time'])
        in_transit_qty = int(request.form['Transit Quantity'])
        forecast_3 = int(request.form['3 Months forecast'])
        forecast_6 = int(request.form['6 Months forecast'])
        forecast_9 = int(request.form['9 Months forecast'])
        sales_1 = int(request.form['1 Month Sales'])
        sales_3 = int(request.form['3 Month Sales'])
        sales_6 = int(request.form['6 Month Sales'])
        sales_9 = int(request.form['9 Month Sales'])
        min_bank = int(request.form['Minimum Stock'])
        pieces_past_due = int(request.form['Pieces past due'])
        perf_6 = float(request.form['6 month performance'])
        perf_12 = float(request.form['12 month performance'])
        local_qty = int(request.form['Local quantity'])

        if( request.form.get('Potential Issue') ):
            potential_issue = 1
        else:
            potential_issue = 0

        if( request.form.get('Deck risk') ):
            deck_risk = 1
        else:
            deck_risk = 0

        if( request.form.get('Oe constraint') ):
            oe_constraint = 1
        else:
            oe_constraint = 0

        if( request.form.get('Ppap risk') ):
            ppap_risk = 1
        else:
            ppap_risk = 0

        if( request.form.get('Stop auto buy') ):
            stop_auto_buy = 1
        else:
            stop_auto_buy = 0

        if( request.form.get('Rev stop') ):
            rev_stop = 1
        else:
            rev_stop = 0

        data = np.array([[national_inv, lead_time, in_transit_qty, forecast_3, forecast_6, forecast_9, 
        sales_1, sales_3, sales_6, sales_9, min_bank, potential_issue, pieces_past_due, perf_6, perf_12, 
        local_qty, deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop]])
        
        my_prediction = classifier.predict(data)

        return render_template(r'result.html', prediction=my_prediction)

if __name__ == '__main__':
    app.debug = True
    app.run()