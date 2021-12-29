import pandas as pd
import plotly.graph_objs as go
import requests
import json

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`



def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    

    
    
    
    
    
    
    
    ### ibb açık veri mekanaik süpürme miktarı
    req3 = requests.get("https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=50036dfd-aea5-4f06-832f-f7020fdaaa5a")
    j3 = req3.json()
    
    df3 = pd.DataFrame(j3['result']['records'])
    df3_melted = df3.melt(id_vars=['Ilce'],var_name='Year',value_name='Amount_m2',value_vars=[str(i) for i in range(2004,2021)])
    ###
    graph_one = []
    for district in df3_melted['Ilce'].unique():
        graph_one.append(
          go.Scatter(
          x = [i for i in range(2004,2021)],
          y = df3_melted.loc[df3_melted['Ilce'] == district,'Amount_m2'],
          mode = 'lines',
          name = district
          )      
        )


    layout_one = dict(title = 'İlçe Bazlı Mekanik Süpürme Miktarı',
                xaxis = dict(title = 'Yıl'),
                yaxis = dict(title = 'Atık Miktarı (m2)'),
                )

    ## ibb açık veri hanehalkı ortalama
    req1 = requests.get("https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=25077460-ddfb-45b6-b32c-4615f0ad2d57")
    j1 = req1.json()

    df1 = pd.DataFrame(j1['result']['records']).sort_values(by='Ortalama Hanehalki Buyuklugu',ascending=False) 
    graph_two = []

    graph_two.append(
      go.Bar(
      x = df1['Ilce Adi'],
      y = df1['Ortalama Hanehalki Buyuklugu'],
      )
    )

    layout_two = dict(title = 'İlçe Bazlı Ortalama Hanehalkı Büyüklüğü - 2018',
                xaxis = dict(title = 'İlçeler',),
                yaxis = dict(title = 'Hanehalkı ortalaması (kişi)'),
                )


    #### ibb açık veri okuma yazma oranı
    req2 = requests.get("https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=18dda65a-4689-44df-938e-05d7cfa264d6")
    j2 = req2.json()

    df2 = pd.DataFrame(j2['result']['records'])
    df2['literacy_rate'] = df2['Okuma Yazma Bilen'] / (df2['Okuma Yazma Bilen'] + df2['Okuma Yazma Bilmeyen'] + df2['Bilinmeyen'])
    df2.sort_values(by='literacy_rate', ascending=False, inplace=True)
    #####
    graph_three = []

    graph_three.append(
      go.Bar(
      x = df2['Ilceler'],
      y = df2['literacy_rate'],
      )
    )

    layout_three = dict(title = 'İlçe Bazlı Okuma Yazma Oranı',
                xaxis = dict(title = 'İlçeler',),
                yaxis = dict(title = 'Okuma Yazma Oranı (%)', range=[0.9,1]),
                )
    
    ### ibb açık veri doğalgaz tüketim
    req4 = requests.get("https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=d5fe41b0-3848-4548-9ac7-6e4756c3027b")
    j4 = req4.json()
    
    df4 = pd.DataFrame(j4['result']['records'])
    df4_melted = df4.melt(id_vars=['Ilce'],var_name='Year',value_name='Amount_m3',value_vars=list(df4.columns[:-2].values))
    
    graph_four = [] 
    for district in df4_melted['Ilce'].unique():
        graph_four.append(
          go.Scatter(
          x = list(df4.columns[:-2].values),
          y = df4_melted.loc[df4_melted['Ilce'] == district,'Amount_m3'],
          mode = 'lines',
          name = district
          )      
        )


    layout_four = dict(title = 'İlçe Bazlı Yıllık Doğalgaz Tüketimi',
                xaxis = dict(title = 'Yıl'),
                yaxis = dict(title = 'Tüketim (m3)'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures