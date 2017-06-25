from flask import request, render_template
from gender_pay_gap_app import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import plotly
import numpy as np
from plotly_functions_within_year import load_data, load_reg_data, regression_graph, plotly_edu, plotly_sup, plotly_los
import plotly.graph_objs as go


gender_data=load_data()

@app.route('/')
@app.route('/index')

def graphing():
    my_data=load_data()
    all_reg_data = load_reg_data()
    year = request.args.get('tag')
    if year is None:
        year = 1980
    my_data = my_data[my_data['year'] == int(year)]
    reg_data = all_reg_data[all_reg_data['years_info'] != int(year)]
    selected_reg_data =  all_reg_data[all_reg_data['years_info'] == int(year)] 
    return render_template("index.html",my_edu_plot = plotly_edu(my_data),
    my_plotly_sup = plotly_sup(my_data), my_plotly_los = plotly_los(my_data), my_reg_graph =regression_graph(reg_data,selected_reg_data), year = year)

@app.route('/about-me')
def add_project():
    return render_template('about-me.html')