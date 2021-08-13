"""
Here we work with our website (Web Aplication), we have a virtual environment created before, but sometimes it
can't open, because we did that long ago, some versions have been changed, etc. We delete the old VE and create a new one:
    pip3 install virtualenv
-next to site's folder (1st older or next to templates, static), open a cmd/atom there, or enter the full path to it and:
    ...mysite> python -m venv virtual                    - make a virtual env. folder. (FOR LINUX: venv -> virtualenv)
    ...mysite> virtual\Scripts\pip3 install flask        - install flask on a virtual environment
   1 ...mysite> virtual\Scripts\python site\script1.py   - execute the script with a python from virtual env
-in this new python, we need to install all the other libraries that we are going to use (bokeh, pandas, pandas data reader)
   1 ...mysite> virtual\Scripts\pip3 install bokeh  (it addes numpy)
   1 ...mysite> virtual\Scripts\pip3 install pandas
   1 ...mysite> virtual\Scripts\pip3 install pandas_datareader

   2 ...mysite> virtual\Scripts\activate                - to activate virtenv
   2 <virtual>...mysite> python script1.py              - execute the script with a python from virtual env
   2 <virtual>...mysite> pip3 install bokeh
   2 <virtual>...mysite> pip3 install pandas

We make a new page on our website, next to "homepage" and "about", we want to make a "plot" that contains a whole script
from the previous program. At the end of it we should specify what page and values we return:


We make a new HTML file "plot.html" (here it is used a copied version of about.html)
In new plot.html, we can put the plot in a header or in a body part, no difference, anyway,
we shoud make the placeholder for the plot! (>>> plot.html)

---------------------------------------------------------------------------------
In the "plot.html" we added placeholders, and in the "layouts.html" we added a link "Plot" to go to the "plot.html".
We run the site using virtualenv, and we see that the site is working, so then we:

DEPLOY SITE TO HEROKU:
Make sure that we are in the same directory as our .py file
- install gunicorn in a virtualenv:
    ...site> ..\virtual\Scripts\pip install gunicorn
- make a Procfile without an extension, and in that file type:
    web: gunicorn script1:app    - telling Heroku to use which script and variable holding the flask (script1, app)
- generate a txt file with a list of installed packages (gunicorn is there as well)
    ...site> ..\virtual\Scripts\pip freeze > requirements.txt
- create an empty "runtame.txt" file and type there (Google the Heraku python supported runtime versions):
    python-3.9.0
- log in to heroku:
    ...site> heroku login
    (type any letter and login with your login parameters of your created account: mirkommiki@yahoo.com)
- to see all your previously added apps to heroku:
    ...site> heroku apps
- to add a new app to heroku:
    ...site> heroku create mirkobokeh
- initialize git repository:
    ...site> git init               - it created a .git folder
- add the files to git:
    ...site> git add .
- commit the changes:
    ...site> git commit -m "first commit"       - N files are added/changed
- connect to the added app:
    ...site> heroku git:remote --app mirkobokeh
- check if you are connected to the app(not necessary):
    ...site> heroku info
                                Git URL:        https://git.heroku.com/mirkobokeh.
                                Owner:          mirkommiki@yahoo.com
                                Region:         us
                                Repo Size:      0 B
                                Slug Size:      0 B
                                Stack:          heroku-20
                                Web URL:        https://mirkobokeh.herokuapp.com/
- connect to the added app:
    ...site> git push heroku master      - PUSH THE CHANGEST, UPLOAD FILES, INSTALLS PYTHON VERS., PACKAGES, ETC.
- open the URL of the site/app:
    ...site> heroku open    (or open the url manually https://mirkobokeh.herokuapp.com/)


"""


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2015, 11, 1)
    end = datetime.datetime(2016, 3, 10)

    df = data.DataReader("GOOG", "yahoo", start, end)

    p = figure(x_axis_type="datetime", width=1000, height=300, sizing_mode='scale_width')
    p.title.text = "Candlestick chart"
    p.grid.grid_line_alpha = 0.3

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Open - df.Close)

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low,
              line_color="black")

    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], hours_12,
           df.Height[df.Status == "Increase"],
           fill_color="#CCFFFF", line_color="black")

    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours_12,
           df.Height[df.Status == "Increase"],
           fill_color="#FF3333", line_color="black")


    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]


    return render_template("plot.html",
                           script1=script1,
                           div1=div1,
                           cdn_js=cdn_js)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)