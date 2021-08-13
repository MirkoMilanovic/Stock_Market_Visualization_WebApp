"""
***  GETTING STOCK MARKET DATA, WORLD BANK (like GDP), data from "FRED", "Fama/French",
"OECD", "Eurostat", "EDGAR index"  ***

Getting the data without searching on the web, just using python!

pip3 install pandas_datareader

help(data.DataReader) - we see that this lib supports Google Finance, St. Louis FED (FRED),
                        and Kenneth French's data library among others

- you google for "stock symbol list" for the symbol of the company, or you search on:
https://finance.yahoo.com/trending-tickers/... and data source can be google, yahoo... yahoo can provide
the best temporal resolution of 1 day (a line for each work-day)... you put the start and the end time (as datetime):

    data.DataReader(name="Stock Symbol/ticker", data_source="yahoo", start=???, end=???)

The company has been sold in shares
stock market DF with columns:
Date - which day, month...
Open - open price, on the beginning of the day
High - max price of the day
Low - lowest price of the day
Close - on the end of the day, the last price
Volume - how many shares are sold on this day
Adj Close - close price that are adjusted...
---------------------------------------------------------------------------------------
We will use the CANDLESTICK graph, which contains 2 glyphs: rectangle (open, close) and vertical line(min, max).
If the rectangle is red, that means that "open>close", so the value decreased that day. Green rectangle - increased.
x-axis is date; y-axis is value.
So we use "rectangle "glyph and "segment" glyph
We need to build the structure of our plot. The good praxis is to use a 12hour quad width/12h gap.

rect glyphs: 4 parameters:
x-coordinates (center of the rectangles)
y-coordinates (center of the rectangles)
width of the rectangles

IT IS ALWAYS GOOD TO HAVE SOME INTERMEDIATE RESULTS, A GOOD PRAXIS IS TO MAKE NEW COLUMNS IN A DATAFRAME
------------------------------------------------------------------------------------------

After, we make segments glyphs for the candlesticks: p.segment... It has to be before the rectangles, to stay behind.
We also make a grid more transparent, and stretch the chart through the full window size:
       p.grid.grid_line_alpha = 0.3
       sizing_mode='scale_width'
Instead of the name of the colors, we can use a CSS core instead like #CCFFFF

------------------------------------------------------------------------------------------
CREATING A FLASK WEB APP WITH A BOKEH CHART

A created chart is an HTML file, we can inspect it. Inside the HTML we have the JAVASCRIPT code for the chart itself, 
links for the CSS file (online link), and for the JAVASCRIPT.
So we need 4 things to grab out of the bokeh chart:
1 - a code for a division (HTML element) where the whole chart is put
2 - the javascript section - this HTML element that contains it
3 - the javascript link (header)
(4 - the CSS link (header)   NOT ANYMORE)

              So, now we don't need these lines (they are just to show the results locally):
                     output_file("CS.html")
                     show(p)

To grab those 3 things, we need:
- to grab the 2 scripts we need to:
       from bokeh.embed import components
       components(p)
- this creates a tuple of 2 elements: javascript code and html div code, so we can grab them and use them in our web app:
       script1, div1 = components(p)
- to grab the JS link, we can do inspect and copy it manually, but the better solution is to use a syntax that can
grab it, because when we update the bokeh library, not to have any problems:
       from bokeh.resources import CDN  (Content Delivery Network)
              ...
       script1, div1 = components(p)      # we grab the javascript and html div from bokeh chart
       cdn_js = CDN.js_files      # we grab the javascript link (this creates a list of 3, we grab the 1st, the widget is 2nd)
     * cdn_css = CDN.css_files    # we grab the css link (this creates a list of 2, we grab the 1st, the widget is 2nd)

*In the new bokeh charts, there is no link to the CSS, the CSS code is put in the HTML code manually.

WE USE OUR FLASK WEBSITE PAGE FURTHER TO PUT OUR CHART INSIDE..... (>>> script1.py)
"""

from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

start=datetime.datetime(2015,11,1)
end=datetime.datetime(2016,3,10)

df = data.DataReader("GOOG", "yahoo", start, end)

p = figure(x_axis_type="datetime", width=1000, height=300, sizing_mode='scale_width')
p.title.text = "Candlestick chart"
p.grid.grid_line_alpha = 0.3

def inc_dec(c, o):
       if c > o:
              value="Increase"
       elif c < o:
              value="Decrease"
       else:
              value="Equal"
       return value


df["Status"]=[inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
df["Middle"]=(df.Open + df.Close)/2
df["Height"]=abs(df.Open-df.Close)

hours_12 = 12*60*60*1000

p.segment(df.index, df.High, df.index, df.Low, line_color="black")

p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], hours_12, df.Height[df.Status=="Increase"],
       fill_color="#CCFFFF", line_color="black")

p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], hours_12, df.Height[df.Status=="Increase"],
       fill_color="#FF3333", line_color="black")

script1, div1 = components(p)
cdn_js = CDN.js_files[0]

print(script1)
print(div1)
print(cdn_js)