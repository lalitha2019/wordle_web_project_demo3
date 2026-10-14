import base64
from io import BytesIO
from flask import Flask, render_template, request, session

# CRITICAL FOR PYTHONANYWHERE: Use the non-interactive Agg backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pandas as pd

import wordle_counts as wc
#--------------------------------------------------------------------
# Get initial values
#--------------------------------------------------------------------
years = wc.get_years()

app = Flask(__name__)
app.secret_key = 'LG-Wordle-Counts-101'

def plot_graph(x_values, y_values, plot_title):
    plt.plot(x_values,y_values)
    #Use plt.gca() to target the y-axis and set the major locator
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    for x, y in zip(x_values, y_values):
        plt.annotate(f'({x},{y})', xy=(x,y), xytext=(x,y))
    plt.title(plot_title, color="darkblue")
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close() # Clear the current figure memory
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return plot_base64

@app.route('/')
def index():
    
    return render_template('index.html', years=years, months=wc.month_names, last_date=wc.last_date_str)

@app.route('/show_custom_counts', methods=['GET','POST'])
def show_custom_counts():
    year = request.form.get('year_select')
    month = request.form.get('month_select')
    letter_counts = wc.get_counts_by_month_for_year(int(year), month)
    df = pd.DataFrame(letter_counts, index=wc.letters, columns=wc.positions)
    session['data'] = letter_counts
    session['y'] = year
    session['m'] = month
    clicked_button = request.form.get('show_custom')
    if clicked_button == 'counts':
        # Convert the DataFrame directly into an HTML table string
        table_html = df.to_html(classes='data')
        # Render the template and pass the table string
        return render_template('table_display.html', year=year, month=month, table=table_html)
    else:
        y_values = [sum(item) for item in letter_counts]
        plot_title = f"Total Number of times a letter appeared in answers in {year} {month}"
        plot_base64 = plot_graph(wc.letters, y_values, plot_title)
        # Render the template and pass the table string
        return render_template('graph_display.html', plot_var=plot_base64)

@app.route('/show_graph', methods=['GET','POST'])
def show_graph():
    pos = int(request.form.get('position_select'))
    y_values = [list[pos-1] for list in session.get('data')]
    plot_title = f'Number of times a letter appeared in {wc.positions[pos-1]} place in {session['y']} {session['m']}'
    plot_base64 = plot_graph(wc.letters, y_values, plot_title)
    # Render the template and pass the table string
    return render_template('graph_display.html', plot_var=plot_base64)

if __name__ == '__main__':
    app.run(debug=True)
