from petl import look, fromdb,fromjson,fromdicts,unpackdict,cut, todb, rename, tocsv
# from matplotlib.pyplot import figure
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from pandas import DataFrame
# from plotly.subplots import make_subplots
# from shapely.geometry import Point
# from geopandas import GeoDataFrame
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.figure_factory as ff
# import psycopg2 as pg
# import requests
import urllib.request, json
# import geopandas as gpd

# Data from an API endpoint
jsonurl = urllib.request.urlopen("https://jsonplaceholder.typicode.com/users")
data = json.loads(jsonurl.read())
# print(data)                 # Dict: Data type

#Extract Data
user_tables = fromdicts(data)         # As we are getting dict as the data type

# Sample
# 1 | Leanne Graham | Bret | Sincere@april.biz | : ID, Name, Username, Email
# {'street': 'Kulas Light', 'suite': 'Apt. 556', 'city': 'Gwenborough', 'zipcode': '92998-3874', 'geo': {'lat': '-37.3159', 'lng': '81.1496'}} | : Address
# 1-770-736-8031 x56442 | hildegard.org | : Phone, Website
# {'name': 'Romaguera-Crona', 'catchPhrase': 'Multi-layered client-server neural-net', 'bs': 'harness real-time e-markets'} : Company

# We have nested dictionary for Address and Company field
# Unpacking the Address field to get more details in an organized way
# Here we transform the Address field
# Using Unpack dict
user_tables = unpackdict(user_tables, 'address') # Returns only the values in the nested dictionary
# print(type(user_tables))
# print(user_tables)
# 1 | Leanne Graham | Bret | Sincere@april.biz |: ID, Name, Username, Email
# 1-770-736-8031 x56442 | hildegard.org | : Phone, Website
# {'name': 'Romaguera-Crona', 'catchPhrase': 'Multi-layered client-server neural-net', 'bs': 'harness real-time e-markets'} |: Company
# Address unpacked:
# Gwenborough   | : city
# {'lat': '-37.3159', 'lng': '81.1496'}  | : geo
# Kulas Light | :street
# Apt. 556  | : Suite
# 92998-3874 | : Zipcode

# We still have a nested dictionary in the address field: geo
# Now we unpack the dictionary
user_tables = unpackdict(user_tables, 'geo')
# print(user_tables)


#  1 | Leanne Graham    | Bret      | Sincere@april.biz         |
#  1-770-736-8031 x56442 | hildegard.org |
#  {'name': 'Romaguera-Crona', 'catchPhrase': 'Multi-layered client-server neural-net', 'bs': 'harness real-time e-markets'}|
#  Gwenborough   | Kulas Light       | Apt. 556  | 92998-3874 | -37.3159 | 81.1496   | : Address: All individual values.

# We still have nested dictionary for the company field
# We will unpack it
user_tables = unpackdict(user_tables, 'company')
# print(user_tables)

# We can select certain columns while we transform the data: The columns that are of use for analysis
user_tables = cut(user_tables, 'id', 'name', 'username', 'email', 'phone', 'website', 'city', 'street', 'suite',
                  'zipcode', 'lat', 'lng')
# Here we have dropped the company details are we do not need them for future analysis

# We will rename the columns: Final stage in the Transform stage
user_tables = rename(user_tables, {'id':'ID',
                                   'name':'Name',
                                   'username':'Username',
                                   'email':'Email',
                                   'phone':'Phone',
                                   'website':'Website',
                                   'city':'City Name',
                                   'street':'Street Name',
                                   'suite': 'Suite Number',
                                   'zipcode': 'Zip-Code',
                                   'lat':'Latitude',
                                   'lng':'Longitude'})

# Load data:
tocsv(user_tables, 'users.csv')

# Read the csv file as a dataframe
df = pd.read_csv("users.csv")


# Plot the co-ordinates on world map
fig = plt.figure(figsize = (12,9))
m = Basemap(projection='mill',
           llcrnrlat =  -90,
           urcrnrlat = 90,
           llcrnrlon = -180,
           urcrnrlon = 180,
           resolution = 'c')

lon_x = df['Longitude'].tolist()
lat_y = df['Latitude'].tolist()

m.scatter(lon_x, lat_y, latlon=True)

m.drawcoastlines()
m.drawcountries()


#m.drawparallels(np.arange(-90,90,10), labels=[True, False,False,False])
#m.drawmeridians(np.arange(-180,180,30), labels=[0,0,0,1])
plt.title("User's Location", fontsize=20)
plt.show()
