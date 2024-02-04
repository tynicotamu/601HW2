
import requests
import pandas  as pd
import numpy   as np
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning

import matplotlib.pyplot as plt
from PIL import ImageTk, Image

class StockGUI:
    def __init__(self, guiWin, api_key):
        self.guiWin_ = guiWin
        self.guiWin_.title("STOCK PRICE REVIEW - LAST 100 DAYS")
        self.guiWin_.geometry("630x650+1100+350")
        self.api_key = api_key
        
        # Declares root canvas as a grid of only one row and one column
        self.guiWin_.columnconfigure(0, weight=1)
        self.guiWin_.rowconfigure(0, weight=1)
        # Create a Frame Inside Canvas with 5 pixel padding all around
        self.mainframe = ttk.Frame(self.guiWin_, padding="5 5 5 5")
        self.mainframe.grid(column=0, row=0, sticky=('n', 'w', 'e', 's'))

        # Add Label Widgets to mainframe
        ttk.Label(self.mainframe, text="Symbol").grid(column=0,row=0, sticky='w')
        col2wdt = 10
        # Add Entry Widget for Entering the Stock Symbol
        self.symbol = tk.StringVar()
        self.symbol_entry = ttk.Entry(self.mainframe, width=col2wdt, justify='center', textvariable=self.symbol, font=("Arial", 15, "bold"))
        self.symbol_entry.grid(column=1, row=0, sticky=('w', 'e'))

        # Add Entry Widget for Entering the Closing Price
        ttk.Label(self.mainframe, text="Close Price").grid(column=0,row=1, sticky='w')
        self.close_price = tk.StringVar()
        self.close_price_entry = ttk.Entry(self.mainframe, width=col2wdt, justify='center', textvariable=self.close_price, font=("Arial", 12, "bold"))
        self.close_price_entry.grid(column=1, row=1, sticky=('w', 'e'))

        # Add Entry Widget for Entering the Previous Close
        ttk.Label(self.mainframe, text="Previous Close").grid(column=0,row=2, sticky='w')
        self.p_close_price = tk.StringVar()
        self.p_close_price_entry = ttk.Entry(self.mainframe, width=col2wdt, justify='center', textvariable=self.p_close_price, font=("Arial", 12, "bold"))
        self.p_close_price_entry.grid(column=1, row=2, sticky=('w', 'e'))

        # Add Entry Widget for Entering the Percent Change
        ttk.Label(self.mainframe, text="Percent Change").grid(column=0,row=3, sticky='w')
        self.change = tk.StringVar()
        self.change_entry = ttk.Entry(self.mainframe, width=col2wdt, justify='center', textvariable=self.change, font=("Arial", 12, "bold"))
        self.change_entry.grid(column=1, row=3, sticky=('w', 'e'))

        # Add Entry Widget for Entering the Volume

        ttk.Label(self.mainframe, text="Volume").grid(column=0,row=4, sticky='w')
        self.vol = tk.StringVar()
        self.vol_entry = ttk.Entry(self.mainframe, width=col2wdt, justify='center', textvariable=self.vol, font=("Arial", 12, "bold"))
        self.vol_entry.grid(column=1, row=4, sticky=('w', 'e'))


        # Add Button Widget for Calling stock_close() to Display Quote 
        ttk.Button(self.mainframe, text="Price", cursor="hand2", width=8, command=self.stock_close).grid(column=1, row=5, sticky=('w','e'))

        ttk.Separator(self.mainframe, orient='horizontal').\
                             grid(column=0, row=6, columnspan=4, sticky="EW")
 
        ttk.Label(self.mainframe,text="Last 100 Days").grid(column=0, row=7, sticky='w')
        self.ac = tk.IntVar()
        self.ac.set(0)
        self.ac1 = ttk.Checkbutton(self.mainframe, text="Adjusted Close", 
                                  variable=self.ac, command=self.plt_ac, 
                                  onvalue=1, offvalue=0). \
                                  grid(column=1, row=7, sticky='w')



        self.c = tk.IntVar()
        self.c.set(0)
        self.c1 = ttk.Checkbutton(self.mainframe, text="Closing Price",
                                  variable=self.c, command=self.plt_close,
                                  onvalue=1, offvalue=0). \
                                  grid(column=2, row=7, sticky='w')

        self.v = tk.IntVar()
        self.v.set(0)
        self.v1 = ttk.Checkbutton(self.mainframe, text="Volume",
                                  variable=self.v, command=self.plt_vol,
                                  onvalue=1, offvalue=0). \
                                  grid(column=3, row=7, sticky='w')




        self.imgwin = ttk.Label(self.mainframe, image="").grid(column=0, 
                                            row=8, columnspan=4, sticky='w')
        
        #Create Frame for Checkbuttons on Right Side
        self.stock_frame = ttk.Frame(self.mainframe, padding=(50, 5, 5, 5),
                                      relief='sunken', borderwidth=5)
        self.stock_frame.grid(column=2, columnspan=2, row=0, rowspan=6, 
                                      sticky=('n', 'w', 'e', 's'))


        self.s1 = tk.IntVar()
        self.s1.set(0)
        self.sc1 = ttk.Checkbutton(self.stock_frame, text="FORD", variable=self.s1, command=self.stock1, onvalue=1, offvalue=0).\
                                  grid(column=0, row=1, sticky='w')

        self.s2 = tk.IntVar()
        self.s2.set(0)
        self.sc2 = ttk.Checkbutton(self.stock_frame, text="GM", variable=self.s2, command=self.stock2, onvalue=1, offvalue=0).\
                                  grid(column=0, row=2, sticky='w')

        self.s3 = tk.IntVar()
        self.s3.set(0)
        self.sc3 = ttk.Checkbutton(self.stock_frame, text="STELLANTIS", variable=self.s3, command=self.stock3, onvalue=1, offvalue=0).\
                                  grid(column=0, row=3, sticky='w')


        self.s4 = tk.IntVar()
        self.s4.set(0)
        self.sc4 = ttk.Checkbutton(self.stock_frame, text="TESLA", variable=self.s4, command=self.stock4, onvalue=1, offvalue=0).\
                                  grid(column=0, row=4, sticky='w')

        self.stocks = ['F', 'GM', 'STLA', 'TSLA']


    def stock_clear(self):
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)
    def stock1(self):
        self.stock_clear()
        self.s1.set(1)
        self.symbol.set(self.stocks[0])
        self.stock_stat()
        self.graph_ts()
    def stock2(self):
        self.stock_clear()
        self.s2.set(1)
        self.symbol.set(self.stocks[1])
        self.stock_stat()
        self.graph_ts()
    def stock3(self):
        self.stock_clear()
        self.s3.set(1)
        self.symbol.set(self.stocks[2])
        self.stock_stat()
        self.graph_ts()
    def stock4(self):
        self.stock_clear()
        self.s4.set(1)
        self.symbol.set(self.stocks[3])
        self.stock_stat()
        self.graph_ts()

    """ Clear Entry Boxes then Update with New Data """  
    def stock_close(self):
        self.stock_clear()
        self.stock_stat()
        if self.symbol != "":
            self.clear_price_button()

    """ Obtain New Stock Data from Alpha Vantage, Requires an API Key """ 
    """ After Obtaining New Data, Update 4 GUI Entry Boxes            """ 
    def stock_stat(self) : 
        # Check for missing stock symbol
        if self.symbol.get() == "":
            showinfo(title="Warning", message="Symbol Missing")
            self.clear_entries()
            return
        c_symbol = self.symbol.get().upper()
        self.symbol.set(c_symbol)
        # base_url variable store base url  
        base_url = \
        r"https://www.alphavantage.co/query?function=GLOBAL_QUOTE"

        # main_url variable store complete url 
        main_url = base_url + "&symbol=" + c_symbol + "&apikey=" + \
                                                    self.api_key      
        # get method of requests module returns response object  
        res_obj = requests.get(main_url) 
        # json method returns json as a python dictionary data type.
        # rates are returned in a list of nested dictionaries.
        self.result = res_obj.json()
        try:
            # Get and Display Last Closing Price
            self.c_price = self.result["Global Quote"]['05. price']
            f_price = round(float(self.c_price), 2)
            self.c_price = str(f_price)
            self.close_price.set("$"+self.c_price)
            
            # Get and Display Previous Day's Closing Price
            self.pc_price = self.result["Global Quote"]['08. previous close']
            f_price = round(float(self.pc_price), 2)
            self.pc_price = str(f_price)
            self.p_close_price.set("$"+self.pc_price)
            
            # Get and Display Percent Change in Stock Value
            self.p_change = self.result["Global Quote"]['10. change percent']
            self.change.set(self.p_change)
            
            # Get and Display Last Day's Volume for this Stock
            self.volume = self.result["Global Quote"]['06. volume']
            v = int(self.volume) # converts the string self.volume to integer
            v = "{:,}".format(v) # converts int to string with commas
            self.vol.set(v)

        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()
            
    """ Clear All 5 GUI Entry Boxes and Any Existing Graph """ 


    def clear_price_button(self):
        self.ac.set(0)
        self.c.set(0)
        self.v.set(0)
        self.imgwin = ttk.Label(self.mainframe, text="").\
                           grid(column=0, row=4, columnspan=8, sticky='w')
        self.imgobj = None

    def clear_entries(self):
        self.stock_clear()
        self.symbol.set("")
        self.close_price.set("")
        self.p_close_price.set("")
        self.change.set("")
        self.vol.set("")
        self.ac.set(0)
        self.c.set(0)
        self.v.set(0)
        self.imgwin = ttk.Label(self.mainframe, text="").\
                           grid(column=0, row=4, columnspan=8, sticky='w')
        self.imgobj = None

    """ Get the Daily Stock Data from Alpha Vantage and then Organize """
    """ this data into a Pandas Dataframe and Save that as self.df    """
    def get_series(self):
        # Check for missing stock symbol
        if self.symbol == "":
            showinfo(title="Warning", message="Symbol Missing")
            return
        c_symbol = self.symbol.get().upper()
        # base_url variable store base url  
        base_url = \
            r"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
    
        # main_url variable store complete url 
        main_url = base_url + "&symbol="+c_symbol+'&outputsize=compact'+"&apikey="+self.api_key
        try:
            # get method of requests module returns response object  
            res_obj = requests.get(main_url) 
            # json returns data in a python dictionary format
            # rates are returned in a list of nested dictionaries  
            result = res_obj.json()
            series = result['Time Series (Daily)']
        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()
            return
        n = len(series)
        f_array = np.array([[0.0]*4]*n)
        i_array = pd.Series([0]*n)
        t_array = pd.Series([pd.to_datetime("2020-01-01")]*n)
        i = n-1
        
        for key in series:
            t_array.loc[i] = pd.to_datetime(key, utc=False)
            i_array.loc[i] = int(series[key]['5. volume'])
            # note the adjusted close is only available using the premium key
            f_array[i][0] = round(float(series[key]['2. high']),  2)
            f_array[i][1] = round(float(series[key]['4. close']), 2)
            f_array[i][2] = round(float(series[key]['3. low']),   2)
            f_array[i][3] = round(float(series[key]['2. high']),  2)
            i-=1
            
        df0 = pd.DataFrame(t_array, columns=['date'])
        df1 = pd.DataFrame(f_array, columns = \
                          ['adjusted_close', 'close', 'low', 'high'])
        df2 = pd.DataFrame(i_array, columns=['volume'])
    
        self.df    = pd.concat([df0, df1, df2], axis=1).set_index('date')
        start_date = self.df.index[0].date()
        end_date   = self.df.index[-1].date()
        print("\n", self.symbol.get(),"Trading days from",  
                                          start_date, "to", end_date, "\n")
        print(self.df.head(2), "\n")
        print(self.df.tail(2))
        
    """ Graph the Selected Time Series in the Bottom Frame """
    def graph_ts(self):
        self.get_series()
        # Check for missing stock symbol
        if self.symbol.get() == "":
            showinfo(title="Warning", message="Symbol Missing")
            self.clear_entries()
            return

        if self.c.get()==1:
            # plot close price
            title = "Closing Price"
            graph = "close"
        elif self.v.get()==1:
            # plot volume
            title = "Volume"
            graph = "volume"
        elif self.ac.get()==1:
            # plot change
            title = "Adjusted Close"
            graph = "adjusted_close"
        else:
            return
        
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.fig.patch.set_facecolor('gray')
        self.fig.patch.set_alpha(0.3)
        font1 = {'family':'Arial','color':'maroon','size': 16,
                 'weight':'normal'}
        font2 = {'family':'Arial','color':'maroon','size': 14,
                 'weight':'normal'}
        gp = self.fig.add_subplot(1,1,1)
        gp.set_facecolor('maroon')
        gp.plot(self.df[graph], color='white')

        start_date = str(self.df.index[0].date())
        end_date   = str(self.df.index[-1].date())

        c_symbol   = self.symbol.get().upper() + \
                             " ("  + start_date + " to "  + end_date+")"
                             
        base_url = \
          r"https://www.alphavantage.co/query?function=SYMBOL_SEARCH"
    
        # main_url variable store complete url 
        main_url = base_url + "&keywords="+self.symbol.get()+ \
                        "&apikey="+self.api_key     
        try:
            # get method of requests module returns response object  
            res_obj = requests.get(main_url) 
            # json returns data in a python dictionary format 
            # rates are returned in a list of nested dictionaries 
            result        = res_obj.json()
            first_company = result['bestMatches'][0]
        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()
            return
        name  = first_company["2. name"]
        score = float(first_company["9. matchScore"])
        if score > 0.9:
            plt.title(name, fontdict=font1)
        else:
            plt.title(c_symbol, fontdict=font1)
        score = float(first_company["9. matchScore"])
        plt.title(name,   fontdict=font1)
        plt.ylabel(title, fontdict=font2)
        plt.grid(True)
        plt.savefig('ts_plot.png')
        plt.show()
        """ Create an Image Object then store the graph in a png file """
        self.imgobj = ImageTk.PhotoImage(Image.open('ts_plot.png'))
        """ Place the graphics image in the bottom of self.mainframe  """
        self.imgwin = ttk.Label(self.mainframe, image=self.imgobj). \
                        grid(column=0, row=9, columnspan=4, sticky='w')

    def plt_close(self):
        self.c.set(1)
        self.v.set(0)
        self.ac.set(0)
        self.graph_ts()
        
    def plt_vol(self):
        self.c.set(0)
        self.v.set(1)
        self.ac.set(0)
        self.graph_ts()
        
    def plt_ac(self):
        self.c.set(0)
        self.v.set(0)
        self.ac.set(1)
        self.graph_ts()
# Instantiate GUI Canvas Using Tk   

root = tk.Tk()
api_key         = "IZHAYZFSN4A3I5OY"
# Paint Canvas Using Class StockGUI __init__()
my_gui = StockGUI(root, api_key)
#Display GUI
root.mainloop()

