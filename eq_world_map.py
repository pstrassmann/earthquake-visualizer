import json
from plotly.graph_obs import Scattergeo, Layout
from plotly import offline

# Map the earthquakes
data = [Scattergeo(lon=lons, lat=lats)]
my_layout = Layout(title='Globbal Earthquakes')

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='global_earthquakes.html')
