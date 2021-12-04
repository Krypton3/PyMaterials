from flask import Flask
import datetime
from polygon import RESTClient

app = Flask(__name__)


@app.route('/stock')
def main():
    key = "your-polygon-key"

    with RESTClient(key) as client:
        from_ = "2021-01-01"
        to = "2021-01-"
        resp = client.stocks_equities_aggregates("AMZN", 1, "minute", from_, to, unadjusted=False)

        return {
            "Durantion" : "Minute aggregates for " + resp.ticker + " between " + from_ + " and " + to,
            "result" : resp.results
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)