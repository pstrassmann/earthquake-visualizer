import datetime

import requests
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

# Retrieve data for all Magnitude 1+ earthquakes in last 30 days
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
data = {
    'format': 'geojson',
    'minmagnitude': '1',
}
r = requests.get(url, data)
if r.status_code != 200:
    raise Exception("Error retrieving data from USGS endpoint")
all_eq_data = r.json()

# Parse earthquake data
def epoch_to_readable_time(epoch_time, date_format='%I:%M %p, %a %B %d, %Y'):
    """ Converts an epoch time in ms and returns a formatted datetime string"""
    epoch_time /= 1000  # from milliseconds to seconds
    return datetime.datetime.fromtimestamp(epoch_time).strftime(date_format)

all_eq_dicts = all_eq_data['features']
month_date_fmt = "%b %d"
end_date = epoch_to_readable_time(all_eq_dicts[0]['properties']['time'], date_format=month_date_fmt)
start_date = epoch_to_readable_time(all_eq_dicts[-1]['properties']['time'],date_format=month_date_fmt)
data_title = f'USGS Earthquakes, {start_date} to {end_date}'

mags, lons, lats, hover_texts = [], [], [], []
for eq_dict in all_eq_dicts:
    mags.append(eq_dict['properties']['mag'])
    lons.append(eq_dict['geometry']['coordinates'][0])
    lats.append(eq_dict['geometry']['coordinates'][1])
    time = epoch_to_readable_time(eq_dict['properties']['time'])
    title = eq_dict['properties']['title']
    hover_texts.append(f"{time}<br>{title}")

# Map the earthquakes
data = [{
    'type': 'scattergeo',
    'text': hover_texts,
    'lon': lons,
    'lat': lats,
    'marker': {
        'size': [3 * mag for mag in mags],
        'color': mags,
        'colorscale': 'Hot',
        'reversescale': True,
        'colorbar': {'title': 'Magnitude'},
    },
}]
my_layout = Layout(
    title={'text': data_title,
           'y': 0.9,
           'x': 0.45,
           'xanchor': 'center',
           'yanchor': 'top'},
    font=dict(size=24))

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='global_earthquakes.html')



