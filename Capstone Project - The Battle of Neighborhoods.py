
# coding: utf-8

# First of all we will import the required libraries.

# In[67]:


from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

# libraries for displaying images
from IPython.display import Image, display 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

#!conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

print('Libraries imported.')


# To get Foursquare data, we use CLIENT_ID and CLIENT_SECRET, which we get from Foursquare. 

# In[2]:


CLIENT_ID = '115N3XYYUZGF2TIJCZBVDRYHKA2IZV34GZJ4EFZKZH1GR3MG' # your Foursquare ID
CLIENT_SECRET = '2VA10XHJF4M1MB2SXVZ4U3Z540CZLD52KXY0FA1JFCUSRO3T' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# Then we get the latitude and longitude for Aleppo and Damascus using geolocator

# In[5]:


Al_address = 'Aleppo'
Dms_address = 'Damascus'
geolocator = Nominatim()
Al_location = geolocator.geocode(Al_address)
Al_latitude = Al_location.latitude
Al_longitude = Al_location.longitude
print("Aleppo latitude is {} , Aleppo longitude is {}".format(Al_latitude,Al_longitude))
Dms_location = geolocator.geocode(Dms_address)
Dms_latitude = Dms_location.latitude
Dms_longitude = Dms_location.longitude
print("Damascus latitude is {} , Damscuslongitude is {}".format(Dms_latitude,Dms_longitude))


# Then we create the required URLs to get data from  foursquare

# In[6]:


radius = 20000
LIMIT = 100
Al_url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, Al_latitude, Al_longitude, VERSION, radius, LIMIT)
Dms_url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, Dms_latitude, Dms_longitude, VERSION, radius, LIMIT)


# Getting the json files of the two cities:

# In[81]:


Al_results = requests.get(Al_url).json()
Dms_results = requests.get(Dms_url).json()


# Then we assign relevant part of JSON to venues and tranform venues into a dataframes

# In[82]:


# assign relevant part of JSON to venues
Al_venues = Al_results['response']['venues']

# tranform venues into a dataframe
Al_df = json_normalize(Al_venues)
display(Al_df.head())
Dms_venues = Dms_results['response']['venues']

# tranform venues into a dataframe
Dms_df = json_normalize(Dms_venues)
display(Dms_df.head())


# We need some columns from theses dataframes and not all columns, so we make new dataframes including these columns.

# In[83]:


filtered_columns = ['name', 'categories'] + [col for col in Al_df.columns if col.startswith('location.')] + ['id']
Al_df_filtered = Al_df.loc[:, filtered_columns]
Dms_df_filtered = Dms_df.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
Al_df_filtered['categories'] = Al_df_filtered.apply(get_category_type, axis=1)
Dms_df_filtered['categories'] = Dms_df_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
Al_df_filtered.columns = [column.split('.')[-1] for column in Al_df_filtered.columns]
Dms_df_filtered.columns = [column.split('.')[-1] for column in Dms_df_filtered.columns]


Al_df_filtered = Al_df_filtered[pd.notnull(Al_df_filtered['categories'])]
Dms_df_filtered = Dms_df_filtered[pd.notnull(Dms_df_filtered['categories'])]
filtered_columns = ['name', 'categories','lat', 'lng'] 
Al_df_filtered = Al_df_filtered.loc[:, filtered_columns]
Dms_df_filtered = Dms_df_filtered.loc[:, filtered_columns]
display(Al_df_filtered.head(3))
display(Dms_df_filtered.head(3))


# We are interested just in hotles or in places that have Hotel in categories feild.

# In[84]:


Al_df_filtered = Al_df_filtered.loc[Al_df_filtered['categories']== "Hotel", :].reset_index(drop=True)
Dms_df_filtered = Dms_df_filtered.loc[Dms_df_filtered['categories']== "Hotel", :].reset_index(drop=True)


# We have 9 hotels in Aleppo

# In[85]:


Al_df_filtered


# We have 3 hotels in Damascus

# In[86]:


Dms_df_filtered


# Then we will show the map that includes the hotels and the center of each city.
# The center location of the map will be the mean of the locations of the two cities. 

# In[94]:


latitude, longitude = (Al_latitude+ Dms_latitude)/2., (Al_longitude+Dms_longitude)/2.
venues_map = folium.Map(location=[latitude, longitude], zoom_start=7) 

# add a red circle marker to represent Aleppo
folium.features.CircleMarker(
    [Al_latitude, Al_longitude],
    radius=10,
    color='red',
    popup='Aleppo',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)
# add a red circle marker to represent Damascus
folium.features.CircleMarker(
    [Dms_latitude, Dms_longitude],
    radius=10,
    color='red',
    popup='Damascus',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

# add the hotels as blue circle markers
for lat, lng, label in zip(Al_df_filtered.lat, Al_df_filtered.lng, Al_df_filtered.name):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)
for lat, lng, label in zip(Dms_df_filtered.lat, Dms_df_filtered.lng, Dms_df_filtered.name):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)

# display map
display(venues_map)


# Then we join the two dataframes in one dataframe. The city isn't shown in the dataframe.

# In[95]:


cities_grouped= pd.concat([Dms_df_filtered, Al_df_filtered])
display(cities_grouped)


# Then we will cluster the hotels into two clusters using KMeans. 
# First we drop 'name' and 'categories' columns and keep just columns tgat help us to make clustering: name , lat, and lng.
# Obviosly the center of each cluster will be in one city different from the other. This will be just an experiment. In real life, there will be more than two cities, and there may be some hotels out of the cities. KMeans helps to solve these problems. 

# In[96]:


kclusters = 2

cities_grouped_clustering = cities_df.drop('name', 1)
cities_grouped_clustering = cities_grouped_clustering.drop('categories', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(cities_grouped_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[:] 


# Check cluster centers

# In[97]:


kmeans.cluster_centers_.tolist()


# Then we add an column including cluster label for each hotel.

# In[98]:


cities_grouped['Cluster Labels'] = kmeans.labels_


# In[99]:


x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
print(x,ys)


# Then we will show a map with different colors for different clusters or hotels in different clusters.

# In[122]:


map_clusters = folium.Map(location=[latitude, longitude], zoom_start=7)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(cities_grouped['lat'], cities_grouped['lng'], cities_grouped['name'], cities_grouped['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
for lat, lon, poi, cluster in zip(cities_grouped['lat'], cities_grouped['lng'], cities_grouped['name'], cities_grouped['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)

    
from IPython.display import IFrame
mapWidth, mapHeight = (400,500) # width and height of the displayed iFrame, in pixels
e = map_clusters.save('spst.html')
#map_clusters.create_map(path='maps/dbscanclusters.html')
IFrame('spst.html',width=700,height=350)


# In[119]:


map_poi = folium.Map()
vega = folium.Vega(json.loads(densities[i].to_json()), width=350,height=200)
popup = folium.Popup(max_width=350).add_child(vega)
circle = folium.CircleMarker(location=[centers[i,0], centers[i,1]], radius=100, popup=popup)
map_poi.add_children(circle)

map_poi.create_map(path='maps/dbscanclusters.html')
IFrame('maps/dbscanclusters.html',width=700,height=350)

