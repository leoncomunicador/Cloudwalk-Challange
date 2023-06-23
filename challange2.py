from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
DATABASE = 'monitoring.db'


def initialize_database():
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            time TEXT,
            status TEXT,
            count INTEGER
        )
        """
    )
    conn.close()

    # Load and insert data from transactions_1.csv
    transactions_1_data = load_transaction_data('files/transactions_1.csv')
    transactions_1_data = transactions_1_data.rename(columns={'f0_': 'count'})
    insert_transaction_data(transactions_1_data)

    # Load and insert data from transactions_2.csv
    transactions_2_data = load_transaction_data('files/transactions_2.csv')
    insert_transaction_data(transactions_2_data)


def load_transaction_data(file_path):
    df = pd.read_csv(file_path)
    df['time'] = pd.to_datetime(df['time'], format="%Hh %M").dt.strftime("%H:%M")
    return df


def insert_transaction_data(dataframe):
    conn = sqlite3.connect(DATABASE)
    dataframe.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()


def retrieve_transaction_data():
    conn = sqlite3.connect(DATABASE)
    query = "SELECT * FROM transactions"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def generate_alerts(dataframe):
    alerts = []

    # Group data by minute and calculate transaction counts
    dataframe = dataframe.groupby(['time', 'status']).sum().reset_index()

    # Check for anomalies and generate alerts
    for index, row in dataframe.iterrows():
        time = row['time']
        status = row['status']
        count = row['count']

        if status == 'failed' and count > 10:
            alerts.append(f"Alert: Failed transactions above normal at {time}. Count: {count}")

        if status == 'reversed' and count > 10:
            alerts.append(f"Alert: Reversed transactions above normal at {time}. Count: {count}")

        if status == 'denied' and count > 10:
            alerts.append(f"Alert: Denied transactions above normal at {time}. Count: {count}")

    return alerts


@app.route("/monitoring", methods=["POST"])
def monitoring():
    transaction_data = request.get_json()
    df = pd.DataFrame(transaction_data)
    insert_transaction_data(df)

    # Retrieve all transaction data
    transaction_data = retrieve_transaction_data()

    # Generate alerts
    alerts = generate_alerts(transaction_data)

    return render_template('index.html', alerts=alerts, transaction_data=transaction_data)


if __name__ == "__main__":
    initialize_database()
    app.run()
