__author__ = 'jesusandrescastanedasosa'
import yahoostocks
import math
import numpy
import matplotlib, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import datetime
import tkinter
from tkinter import ttk
matplotlib.use('TkAgg')


def _quit():
    root.quit()
    root.destroy()

def destroy(e): sys.exit()

def historical(stocks=['GOOG','YHOO','GE'], from_date={'month':1, 'day': 1, 'year':2000}, to_date={'month':-1}):
    #Graphs closing value of the day
    for i, stock in enumerate(stocks):
        response = numpy.array([ n[6] for n in yahoostocks.historical(stock, from_date, to_date)])
        plt.plot([ n for n in range(1,len(response)+1) ], response)
        if i == 0:
            x_label = "Days from "+\
                str(from_date['month'])+"/"+\
                str(from_date['day'])+"/"+\
                str(from_date['year'])+"/"+\
                " to "+\
                str(to_date['month'])+"/"+\
                str(to_date['day'])+"/"+\
                str(to_date['year'])+"/"
            plt.xlabel(x_label)
            plt.ylabel("Closing Price")
    plt.legend([n[0] for n in yahoostocks.current(stocks)], loc='upper left')
    plt.show()
    return True

def realtime(stocks=['GOOG'], range='1d'):
    figure.clf()
    figure_sub = figure.add_subplot(111)
    for i,stock in enumerate(stocks):
        response = yahoostocks.realtime(stock,range)
        x_axis = [float(n[0]) for n in response]
        times = [datetime.datetime.fromtimestamp(n) for n in x_axis]
        y_axis = [float(n[1]) for n in response]
        #positino 1 is the closed price
        figure_sub.plot(x_axis, y_axis)
        if i==0:
            ticks_x = []
            for i, n in enumerate(times):
                if i % 50 == 0:
                    ticks_x.append([i, n])
            ticks_x1 = [x_axis[n[0]] for n in ticks_x]
            ticks_x2 = [str(n[1].hour)+":"+str(n[1].minute) for n in ticks_x]
            # figure_sub.xticks(ticks_x1, ticks_x2)
            # matplotlib.axes.set_xticks(ticks_x2, minor=False)
            #     majorLocator = matplotlib.ticker.FixedLocator(ticks_x1)
            #     figure_sub.xaxis.set_major_locator(majorLocator)
            figure_sub.grid(True)
            figure_sub.set_xticks(ticks_x1)
            figure_sub.set_xticklabels(ticks_x2)
            figure_sub.set_xlabel("Real time stocks by the hour")
            figure_sub.set_ylabel("Closing Price")
    figure_sub.legend([n[0] for n in yahoostocks.current(stocks)], loc='upper left')

    data_plot.show()
    return True


def calculate(*args):
    try:
        stocks_raw = str(stocks.get())
        if stocks_raw is not '':
            stocks_list = stocks_raw.split()
            #write stocks options
            #for new_stock in stocks_list:


            #end write stock options
            realtime(stocks_list)
    except ValueError:
        pass



root = tkinter.Tk()
root.title("Stocks Grapher")
figure = Figure(figsize=(10, 7,), dpi=100)
data_plot = FigureCanvasTkAgg(figure, master=root)
data_plot.get_tk_widget().grid(column = 1, row = 0, sticky='nsew')
data_plot.show()

controls = ttk.Frame(root, padding="10 10 10 10")
controls.grid(column=0, row=0, sticky='nsew')


stocks = tkinter.StringVar()
stocks_entry = ttk.Entry(controls, width='20', textvariable=stocks)
stocks_entry.grid(column=0, row=1, sticky=('w','e'))
ttk.Label(controls, text="Stocks to graph (separate by space):", anchor='w', justify='left').grid(column=0, row=0, sticky=('w','e'))

ttk.Button(controls, text="Graph Stocks", command=calculate).grid(column=0, row=2, sticky=('w','e'))

for child in controls.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=('w','e','n','s'))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)
# stocks = tkinter.StringVar()
# stocks_entry = ttk.Entry(mainframe, width='20', textvariable=stocks)
# stocks_entry.grid(column=2, row=1, sticky=('w','e'))
# ttk.Label(mainframe, textvariable="Stocks").grid(column=3, row=1, sticky='w')
# ttk.Button(mainframe, text="Graph", command=calculate).grid(column=2, row=2, sticky=('w','e'))
# for child in mainframe.winfo_children():
#     child.grid_configure(padx=5, pady=5)
# root.mainloop()