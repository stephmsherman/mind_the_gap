import plotly
from plotly import plotly as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.mlab as mlab
import pandas as pd
import statsmodels.formula.api as smf

def load_data():
    loaded_data=pd.read_csv('/home/ubuntu/application/gender_pay_gap_app/data/gender_edu_data.csv',dtype={"sub_agency": str, "state": str,"pay_grade": str})
    return loaded_data

def load_reg_data():
    loaded_data=pd.read_csv('/home/ubuntu/application/gender_pay_gap_app/data/regression_results_edu.csv')
    return loaded_data

def regression_graph(reg_data, selected_reg_data):
    men_edu = go.Scatter(
    x=reg_data['years_info'],
    y=reg_data['coef_year_inflation'],
    name='',
    mode = 'markers',
    marker = {"size": 12, "color": "#8b8a8a"}
)
    sel = go.Scatter(
    x=selected_reg_data['years_info'],
    y=selected_reg_data['coef_year_inflation'],
    name='',
    mode = 'markers',
    marker = dict(
        size = 20,
         color = "#d95f02",
         symbol = "diamond",
         line = dict(
            width = 4,
            color = "#ffeda0",
        ))
)

    data = [men_edu, sel]
    layout = go.Layout(
    title= 'Adjusted for Education, Leadership and Experience',#'In <b>%s</b> women are paid <b>$%s</b> less than men accounting for </br>Education, Supervisory Status and Years of Experience' %(int(selected_reg_data['years_info']),'{:,}'.format(int(selected_reg_data['coef_year_inflation']))),
    titlefont=dict(
            family='arial',
            size=22,
            color='black'
        ),
    xaxis=dict(
        title='Years',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        tickfont = dict(
        family='arial',
            size=20,
            color='black')
    ),
    yaxis=dict(range=[0,12000],
        title='Gender Pay Gap ($)',
        hoverformat='$,.0f',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        tickfont = dict(
        family='arial',
            size=20,
            color='black')
    ),
    showlegend=False,
    margin=go.Margin(
        l=150,
        r=50,
        b=50,
        t=50,
        pad=1
    ),
)
    fig = go.Figure(data=data, layout=layout)
   # fig['layout']['autosize'] = "False"
    fig['layout']['height'] = 350
    reg_pay_diff_results='{:,}'.format(int(selected_reg_data['coef_year_inflation']))
    div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return {'div': div, 'reg_pay_diff_results': reg_pay_diff_results}



def plotly_edu(loaded_data):
    edu=loaded_data.groupby(['education_level','gender'],as_index=False)['pay_inflation'].mean()
    edu['pay_inflation']=edu['pay_inflation'].round(0)
    men_results=smf.ols(formula ='pay_inflation ~education_level', data = loaded_data[loaded_data['gender']==1]).fit()
    women_results=smf.ols(formula ='pay_inflation ~education_level', data = loaded_data[loaded_data['gender']==0]).fit()
    reg_pay_diff_results = int((men_results.params[1]-women_results.params[1]).round(0))
    reg_pay_diff_results_str = "${:,.2f}".format(reg_pay_diff_results)
    men_slope=loaded_data['education_level'].sort_values().unique() *men_results.params[1] + men_results.params[0]
    women_slope= loaded_data['education_level'].sort_values().unique() *women_results.params[1] + women_results.params[0]
    men_y =edu.loc[edu['gender']==1,'pay_inflation']
    women_y=edu.loc[edu['gender']==0,'pay_inflation']
    
    men_edu = go.Scatter(
    x=edu.loc[edu['gender']==1,'education_level'],
    y=men_y,
    name='Men',
    hoverinfo='none',
    mode = 'markers',
    marker = dict(
        size = 6,
        color = '#1b9e77'))
    men_reg = go.Scatter(
    x=edu.loc[edu['gender']==1,'education_level'],
    y=men_slope,
    name='Men',
    hoverinfo='none',
    line = dict(
        width = 4,
        color = '#1b9e77'
    ),
)
    women_edu = go.Scatter(
    x=edu.loc[edu['gender']==0,'education_level'],
    y=women_y,
    name='Women',
    hoverinfo='none',
    mode = 'markers',
    marker = dict(
        size = 6,
        color = '#7570b3'))
    
    women_reg = go.Scatter(
    x=edu.loc[edu['gender']==0,'education_level'],
    y=women_slope,
    name='Women',
    hoverinfo='none',
    line = dict(
        width = 4,
        color = '#7570b3'
    ),
    #text = map(str,men_y.values - women_y.values)
    
)
    data = [men_edu, women_edu, men_reg, women_reg]
    
    layout = go.Layout(
    title='Women are paid <b>$%s</b> less than men </br>for each level increase in education' %('{:,}'.format(reg_pay_diff_results)),
    titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
    xaxis=dict(
        title='Education Level',
        titlefont=dict(
            family='arial',
            size=20,
            color='black' ),
            showticklabels=True,
            tickvals = [4,10,13,17,21],
            ticktext = ["HS","AA", "BA", "MA","PhD"],
        
        tickangle=0,
        tickfont=dict(
            family='arial',
            size=15,
            color='black'
        ),
       ),
        yaxis=dict(range=[40000,140000],
        title='Salary',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='arial',
            size=15,
            color='black'
        ),
        
        ),
        hovermode = 'closest',
        showlegend=False,
    )
    fig = go.Figure(data=data, layout=layout)
    #fig['layout']['width'] = 700
    #fig['layout']['autosize'] = "False"
    fig['layout']['height'] = 350
    
    div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return {'div': div, 'reg_pay_diff_results': reg_pay_diff_results}

def plotly_sup(loaded_data):
    sup=loaded_data.groupby(['supervisory_status','gender'],as_index=False)['pay_inflation'].mean()
    sup['pay_inflation']=sup['pay_inflation'].round(0)
    men_results=smf.ols(formula ='pay_inflation ~supervisory_status', data = loaded_data[loaded_data['gender']==1]).fit()
    women_results=smf.ols(formula ='pay_inflation ~supervisory_status', data = loaded_data[loaded_data['gender']==0]).fit()
    men_reg=loaded_data['supervisory_status'].sort_values().unique() *men_results.params[1] + men_results.params[0]
    women_reg= loaded_data['supervisory_status'].sort_values().unique() *women_results.params[1] + women_results.params[0]
    sup_difference=int(men_reg[1] - women_reg[1].round(0))
    men_edu = go.Bar(
    x=sup.loc[sup['gender']==1,'supervisory_status'],
    y=sup.loc[sup['gender']==1,'pay_inflation'],
    name='Men',
    hoverinfo='none',
    marker=dict(
        color='#1b9e77',
        line=dict(
            color='black',
            width=.5,
        )
    ),
)
    women_edu = go.Bar(
    x=sup.loc[sup['gender']==0,'supervisory_status'],
    y=sup.loc[sup['gender']==0,'pay_inflation'],
    name='Women',
    hoverinfo='none',
    marker=dict(
        color='#7570b3',
        line=dict(
            color='black',
            width=.5,
        )
    )
)
    data = [men_edu, women_edu]
    
    layout = go.Layout(
    title='As supervisors women </br>are paid <b>$%s</b> less' %('{:,}'.format(sup_difference)),
    titlefont=dict(
            family='arial',
            size=15,
            color='black'
        ),
    xaxis=dict(
        title='Supervisory Status',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        showticklabels=True,
        tickvals = [0,1],
        ticktext = ['No', 'Yes'],
        tickangle=0,
        tickfont=dict(
            family='arial',
            size=15,
            color='black'
        ),
    ),
    yaxis=dict(range=[40000,140000],
        title='Salary',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='arial',
            size=15,
            color='black'
        ),
        
        ),
        hovermode = 'closest',
        showlegend=False
    )
    fig = go.Figure(data=data, layout=layout)
    #fig['layout']['width'] = 700
    fig['layout']['height'] = 350
    fig['layout']['autosize'] = "True"
    div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return div
    
    
def plotly_los(loaded_data):
    los=loaded_data.groupby(['length_of_service','gender'],as_index=False)['pay_inflation'].mean()
    los['pay_inflation']=los['pay_inflation'].round(0)
    men_results=smf.ols(formula ='pay_inflation ~length_of_service', data = loaded_data[loaded_data['gender']==1]).fit()
    women_results=smf.ols(formula ='pay_inflation ~length_of_service', data = loaded_data[loaded_data['gender']==0]).fit()
    men_slope=loaded_data['length_of_service'].sort_values().unique() *men_results.params[1] + men_results.params[0]
    women_slope= loaded_data['length_of_service'].sort_values().unique() *women_results.params[1] + women_results.params[0]
    reg_difference=int((men_results.params[1]-women_results.params[1]).round(0))
    men_edu = go.Scatter(
    x=los.loc[los['gender']==1,'length_of_service'],
    y=los.loc[los['gender']==1,'pay_inflation'],
    name='Men',
    hoverinfo='none',
    mode = 'markers',
    marker = dict(
        size = 6,
        color = '#1b9e77')

)
    men_reg = go.Scatter(
    x=los.loc[los['gender']==1,'length_of_service'],
    y=men_slope,
    name='Men',
    hoverinfo='none',
    line = dict(
        width = 4,
        color = '#1b9e77'
    )

)
    women_edu = go.Scatter(
    x=los.loc[los['gender']==0,'length_of_service'],
    y=los.loc[los['gender']==0,'pay_inflation'],
    name='Women',
    hoverinfo='none',
    mode = 'markers',
    marker = dict(
        size = 6,
        color = '#7570b3')
)
    women_reg = go.Scatter(
    x=los.loc[los['gender']==0,'length_of_service'],
    y=women_slope,
    name='Women',
    hoverinfo='none',
    line = dict(
        width = 4,
        color = '#7570b3'
    )
)
    data = [men_edu, women_edu,men_reg, women_reg]

    
    layout = go.Layout(
    title='Women are paid <b>$%s</b> less than men </br>for every year they stay in their job' %('{:,}'.format(reg_difference)),
    titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
    xaxis=dict(
        title='Years Employed',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='arial',
            size=15,
            color='black'
        ),
    ),
        yaxis=dict(range=[40000,140000],
        title='Salary',
        titlefont=dict(
            family='arial',
            size=20,
            color='black'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='arial',
            size=15,
            color='black'
        ),
        
        ),
        legend =dict(
        x=30,
        y=1.5,
        traceorder='normal',
        font=dict(
            family='arial',
            size=25,
            color='black'
        )
    ),
        hovermode = 'closest',
        showlegend=False,
    )
    fig = go.Figure(data=data, layout=layout)
   # fig['layout']['width'] = 700
    fig['layout']['height'] = 350
    #fig['layout']['autosize'] = "False"
    div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    return div