import pandas as pd
import plotly.graph_objs as go



def cleandata(dataset, keepcolumns = ['Country Name', '2000', '2020'], value_variables = ['2000', '2020']):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """    
    df = pd.read_csv(dataset, skiprows=4)

    # Keep only the columns of interest (years and country name)
    df = df[keepcolumns]

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']
    df = df[df['Country Name'].isin(top10country)]

    # melt year columns  and convert year to date time
    df_melt = df.melt(id_vars='Country Name', value_vars = value_variables)
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt

def return_figures():
    """Creates plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the plotly visualizations

    """

  # first chart plots arable land from 2000 to 2020 in top 10 economies 
  # as a line chart
    
    graph_one = []
    df = cleandata('data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3632113.csv')
    df.columns = ['country','year','GDPpercapita']
    df.sort_values('GDPpercapita', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()
    
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].GDPpercapita.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'GDP per capita from 2000 to 2020',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=2000, dtick=10),
                yaxis = dict(title = 'US$'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    df = cleandata('data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3632113.csv')
    df.columns = ['country','year','GDPpercapita']
    df.sort_values('GDPpercapita', ascending=False, inplace=True)
    df = df[df['year'] == 2020] 

    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].GDPpercapita.tolist()
      graph_two.append(dict(
        type='choropleth',
        locations = df.country.unique().tolist(),
        autocolorscale = True,
        z = df[df['country'] == country].GDPpercapita.tolist(),
        locationmode = 'country names',
        marker = dict(
          line = dict (
            color = 'rgb(255,255,255)',width = 2),
            colorbar = dict(
              title = 'Millions USD'))
              ))
      layout_two = dict(title = 'Top Countries by GDP per capital')
          




# # third chart plots percent of population that is rural from 1990 to 2015
#     graph_three = []
#     df = cleandata('data/API_SP.RUR.TOTL.ZS_DS2_en_csv_v2_9948275.csv')
#     df.columns = ['country', 'year', 'percentrural']
#     df.sort_values('percentrural', ascending=False, inplace=True)
#     for country in countrylist:
#       x_val = df[df['country'] == country].year.tolist()
#       y_val =  df[df['country'] == country].percentrural.tolist()
#       graph_three.append(
#           go.Scatter(
#           x = x_val,
#           y = y_val,
#           mode = 'lines',
#           name = country
#           )
#       )

#     layout_three = dict(title = 'Change in Rural Population <br> (Percent of Total Population)',
#                 xaxis = dict(title = 'Year',
#                   autotick=False, tick0=1990, dtick=25),
#                 yaxis = dict(title = 'Percent'),
#                 )
    

    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    # figures.append(dict(data=graph_three, layout=layout_three))
   

    return figures