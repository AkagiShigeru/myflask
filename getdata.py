# python script to get quandl stock data in json format with requests library
import requests
# from IPython import embed
import numpy as np
import pandas as pd


def GetQuandlData(stock_name, start_date=None, end_date=None):
    api_key = "Wup-DN1STaZ_uvnxVTAQ"  # from my registered quandl account

    sdate = ""
    if start_date is not None:
        sdate += "&start_date=%s" % start_date

    edate = ""
    if end_date is not None:
        edate += "&end_date=%s" % end_date

    # get raw data
    raw = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/%s.json?order=asc&api_key=%s%s%s" % (stock_name, api_key, sdate, edate))

    # parse json into python dictionaries
    json = raw.json()
    data = json["dataset"]["data"]
    cols = json["dataset"]["column_names"]

    # convert to pandas dataframe
    df = pd.DataFrame(data, columns=cols)
    df.set_index("Date", drop=False, inplace=True)

    # try to extract the full name of the stock company
    # fall back to short identifier if it doesn't work
    try:
        name = json["dataset"]["name"].split("(")[0].strip()
    except:
        name = stock_name

    return df, name


def PlotWithBokeh(dates, data_list, names, stock_name):

    from bokeh.layouts import gridplot
    from bokeh.plotting import figure, show, save, output_file

    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    p1 = figure(x_axis_type="datetime", title="Quandl WIKI EOD Stock Prices: %s" % stock_name,
                plot_width=600, plot_height=400)

    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = "Date"
    p1.yaxis.axis_label = "Price"
    p1.xaxis.axis_label_text_font_style = "bold"
    p1.yaxis.axis_label_text_font_style = "bold"

    colors = ["red", "green", "blue", "black", "purple"]

    for i, data in enumerate(data_list):
        p1.line(datetime(dates), data, color=colors[i],
                legend=names[i])

    p1.legend.location = "top_left"

    return p1

    # stock_dates = np.array(dates, dtype=np.datetime64)
    # stock = np.array(data)

    # window_size = 30
    # window = np.ones(window_size) / float(window_size)
    # stock_avg = np.convolve(stock, window, "same")

    # p2 = figure(x_axis_type="datetime", title="Stock One-Month Average")
    # p2.grid.grid_line_alpha = 0

    # p2.xaxis.axis_label = "Date"
    # p2.yaxis.axis_label = "Price"
    # p2.xaxis.axis_label_text_font_style = "normal"
    # p2.yaxis.axis_label_text_font_style = "normal"

    # p2.ygrid.band_fill_color = "olive"
    # p2.ygrid.band_fill_alpha = 0.1

    # p2.circle(stock_dates, stock, size=4, legend="close",
    #           color="darkgrey", alpha=0.2)

    # p2.line(stock_dates, stock_avg, legend="avg", color="navy")
    # p2.legend.location = "top_left"

    # output_file("./templates/plot.html", title="Stock Prices: %s" % stock_name)

    # show(gridplot([[p1, p2]], plot_width=400, plot_height=400))  # open a browser
    # show(p1)  # open a browser
    # save(p1)  # open a browser


# GetQuandlData("AAPL")
