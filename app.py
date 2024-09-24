#!/usr/bin/env python3

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from lib import load_csv, dropdown_params

# Load dataset
file_path = './activities.csv'
df = load_csv(file_path)

# Dropdowns options Setup
summary_params, sport_params, variable_params, year_params = dropdown_params(df)

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout of the app
app.layout = html.Div(

    children=[

        # Title
        html.Div(
            className="header",
            children=[
                html.H1(
                    className="header-title",
                    children=[
                        html.Span('Strav', className='orange'),
                        html.Span('Analyzer', className='white')
                    ],
                ),
                html.P('A useful tool to analyze your Strava activities', className="header-description"),
            ]
        ),

        # Dropdowns Menu
        html.Div(
            className="menu",
            children=[

                # Summary Type Dropdown
                html.Div(
                    className="dropdown",
                    children=[
                        html.Label('Summary Type', className="dropdown-title"),
                        dcc.Dropdown(
                            id='summary-type',
                            options=summary_params[0],
                            value=summary_params[1],
                            clearable=False,
                            className="dropdown-list"
                        ),
                    ],
                ),

                # Sport Dropdown
                html.Div(
                    className="dropdown",
                    children=[
                        html.Label('Sport', className="dropdown-title"),
                        dcc.Dropdown(
                            id='sport',
                            options=sport_params[0],
                            value=sport_params[1],
                            clearable=False,
                            className="dropdown-list"
                        ),
                    ],
                ),

                # Variable Dropdown
                html.Div(
                    className="dropdown",
                    children=[
                        html.Label('Variable', className="dropdown-title"),
                        dcc.Dropdown(
                            id='variable',
                            options=variable_params[0],
                            value=variable_params[1],
                            clearable=False,
                            className="dropdown-list"
                        ),
                    ],
                ),

                # Year Dropdown
                html.Div(
                    className="dropdown",
                    children=[
                        html.Label('Year', className="dropdown-title"),
                        dcc.Dropdown(
                            id='year',
                            options=year_params[0],
                            value=year_params[1],
                            clearable=False,
                            className="dropdown-list"
                        ),
                    ]
                ),
            ]
        ),

        # Graph
        html.Div(
            className="histogram",
            children=[
                dcc.Graph(id='activity-graph')
            ]
        ),
    ]
)


# Callback function to update the graph based on user inputs
@app.callback(
    Output('activity-graph', 'figure'),
    Input('summary-type', 'value'),
    Input('sport'       , 'value'),
    Input('variable'    , 'value'),
    Input('year'        , 'value'),
)
def update_graph(summary_type, sport, variable, year):

    # Filter the data based on selected sport
    local_df = df[(df['Sport'] == sport)] if sport != 'All' else df

    # Group the data based on the selected analysis type
    if summary_type == 'Yearly':

        # Yearly analysis: group by year
        df_to_plot = local_df.groupby('Year', as_index=False)[variable].sum()
        x_label = 'Year'

    elif summary_type == 'Monthly':

        # Monthly analysis: restrict to the selected year and group by month
        local_df = local_df[local_df['Year'] == year]
        grouped_df = local_df.groupby('Month', as_index=False)[variable].sum()
        all_months = pd.DataFrame({'Month': range(1, 13)})
        df_to_plot = pd.merge(all_months, grouped_df, on='Month', how='left').fillna(0)
        
        # set abbreviated names for months instead of integers
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        df_to_plot['Month'] = df_to_plot['Month'].map(month_names)
        x_label = 'Month'

    elif summary_type == 'Weekly':

        # Weekly analysis: restrict to the selected year and group by week
        local_df = local_df[local_df['Year'] == year]
        grouped_df = local_df.groupby('Week', as_index=False)[variable].sum()
        all_months = pd.DataFrame({'Week': range(1, 53)})
        df_to_plot = pd.merge(all_months, grouped_df, on='Week', how='left').fillna(0)
        x_label = 'Week'

    # Create bar plot
    y_label = f'{variable}'
    fig = px.bar(
        df_to_plot,
        x=x_label,
        y=y_label,
        title=f'{y_label} by {x_label}',
        color_discrete_sequence=['#ea580a']
    )

    # Update layout properties
    fig.update_layout(
        title={
            'x': 0.5,
            'y': .95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'weight': 'bold',
                'family': 'Roboto, sans-serif',
                'color': '#222222',
            }
        },
        xaxis=dict(
            titlefont=dict(
                family='Lato, sans-serif',
                size=18,
                color='#222222',
            ),
            tickfont=dict(
                family='Arial, sans-serif',
                size=14,
                color='#222222',
            )
        ),
        yaxis=dict(
            titlefont=dict(
                family='Lato, sans-serif',
                size=18,
                color='#222222',
            ),
            tickfont=dict(
                family='Arial, sans-serif',
                size=14,
                color='#222222',
            )
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        # paper_bgcolor='lightgray',
        # plot_bgcolor='white',
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)