from flask import Flask, render_template, request
from getdata import GetQuandlData, PlotWithBokeh
from bokeh.embed import components
from datetime import datetime
from copy import copy
import dateutil

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        # response.headers['Pragma'] = 'no-cache'

        stock = request.form.get("ticker")
        months = int(request.form.get("months"))
        values = request.form.getlist("features")
        values_ori = copy(values)

        if len(values) == 0:
          return render_template("error.html", reason="No values to plot specified")

        values_map = {"open": "Open", "close": "Close",
                      "adj_close": "Adj. Close", "adj_open": "Adj. Open"}
        values = [values_map[value] for value in values]

        # date stuff
        now = datetime.utcnow()
        then = now - dateutil.relativedelta.relativedelta(months=months)
        now, then = now.strftime("%Y-%m-%d"), then.strftime("%Y-%m-%d")

        try:
            data, sname = GetQuandlData(stock, then, now)
        except:
            return render_template("error.html", reason="Couldn't find and process data for %s" % stock)

        data_list = [data.get(value) for value in values]

        try:
            plot = PlotWithBokeh(data.Date, data_list, values, sname)
        except:
            return render_template("error.html", reason="plotting failed!")

        # directly embedding plot (no plot file is ever written)
        script, div = components(plot)
        return render_template("index.html", script=script, div=div,
                               ticker=stock, months=months,
                               checked_values=values_ori)

    else:
        return render_template("index.html", ticker="AAPL", months=6,
                               checked_values=["close"])


# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r


if __name__ == "__main__":
    app.run(port=33507)
