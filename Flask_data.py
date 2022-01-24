from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    PATH = 'C:/Franz/UCA_M2/Thales/code/Copernicus_Project/data/try_1/format_data/Training_merged_DB_v4r.csv'
    df = pd.read_csv(PATH, sep=',', encoding='latin-1')
    df.columns = [c.replace('(', '') for c in df.columns]
    df.columns = [c.replace(')', '') for c in df.columns]
    df.columns = [c.replace(' ', '') for c in df.columns]
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]

    items = df.to_dict('records')
    return render_template('market.html', items=items)