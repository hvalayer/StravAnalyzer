#!/usr/bin/env python3

#===================================================================================================================================
# AUXILIARY LIB
#===================================================================================================================================

import pandas as pd

# convert seconds to hours:minutes:seconds
def s_to_hms(s):
    h, tmp = divmod(s, 3600)
    m, s = divmod(tmp, 60)
    return "%i:%02i:%02i" %(h,m,s)

# compute pace (in km/h and min/km) from distance (m) and time (s)
def compute_pace(d, t):
    if t<1.0:
        return 0.0, 0.0
    else:
        out1 = d/t*3.6
        tmp = t/d*10**3
        m, s = divmod(tmp, 60)
        out2 = "%2i:%02i min/km" %(m,s)  
        return out1, out2

# load a dataset (CSV format) and create a clean pandas dataframe
def load_csv(file):

    # read original file
    df = pd.read_csv(file)

    # columns to keep
    c_to_keep = [
        'Activity Date',
        'Activity Type',
        'Elapsed Time.1',
        'Moving Time',
        'Distance.1',
        'Elevation Gain',
        'Average Heart Rate',
        'Activity Gear'
    ]

    # extract desired columns
    df = df[c_to_keep]

    # rename some columns
    c_names = {
        'Activity Date'     : 'Date',
        'Activity Type'     : 'Sport',
        'Elapsed Time.1'    : 'Elapsed Time',
        'Distance.1'        : 'Distance',
        'Elevation Gain'    : 'Elevation',
        'Activity Gear'     : 'Gear',
    }
    df.rename(columns=c_names, inplace=True)

    # set date format
    date_format = '%b %d, %Y, %I:%M:%S %p'

    # convert date to datetime format
    formatted_col = pd.to_datetime(df['Date'], format=date_format)
    df = df.assign(Date=formatted_col)

    # sort by date
    df = df.sort_values(by='Date')

    # split date into year, month and week
    df['Year']  = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Week']  = df['Date'].dt.isocalendar().week

    # correct elevation gain: if NaN then 0.0
    df['Elevation'] = df['Elevation'].fillna(0.0)

    # correct activity gear: if NaN then 'unknown'
    df['Gear'] = df['Gear'].fillna('Unknown')

    return df

# Set Dropdowns Parameters
def dropdown_params(df):

    # Summary Type Dropdown Parameters
    options = [
        {'label': 'Yearly'  , 'value': 'Yearly' },
        {'label': 'Monthly' , 'value': 'Monthly'},
        {'label': 'Weekly'  , 'value': 'Weekly' }
    ]
    default = 'Yearly'
    summary_params = (options, default)

    # Sport Dropdown Parameters
    options = [{'label': sport, 'value': sport} for sport in df['Sport'].unique()]
    options = sorted(options, key=lambda x: x['label'])
    options.insert(0, {'label': 'All', 'value': 'All'})
    default = 'All'
    sport_params = (options, default)

    # Variable Dropdown Parameters
    options = [
        {'label': 'Distance'    , 'value': 'Distance'           },
        {'label': 'Moving Time' , 'value': 'Moving Time'        },
        {'label': 'Elapsed Time', 'value': 'Elapsed Time'       },
        {'label': 'Elevation'   , 'value': 'Elevation'          },
        # {'label': 'Heart Rate'  , 'value': 'Average Heart Rate' }
    ]
    default = 'Distance'
    variable_params = (options, default)

    # Year Dropdown Parameters
    options = [{'label': year, 'value': year} for year in df['Year'].unique()]
    default = max(option['value'] for option in options)
    year_params = (options, default)

    return summary_params, sport_params, variable_params, year_params