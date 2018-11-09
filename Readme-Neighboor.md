# Introduction/Business Problem

# 1- A description of the problem and a discussion of the background

We will recommend the best places to set up offices for a taxi company, trying to start its own business, that provides services to hotel guests.

To achieve a good start for any new business, it is important to accurately define market requirements first. In the taxi office case, most requests may come from foreign people or from people who have a lot of moves and do not have a car.This kind of people often live in hotels. Therefore, it is best to choose the location of the taxi office so that the distance is as low as possible from hotels in the city. 

Since we are not bound by an option, we will choose cities from Syria (as it's my country) to solve this problem. We will choose two cities (Aleppo and Damascus). The two cities will be treated as one place. After that, the system should find the best places for locating two taxi offices. Each of these two places obviously must be in a different city from the other. We want to get this result using K Means, getting centers at an equal distance from hotels in the city.

# 2- A description of the data and how it will be used to solve the problem.

First we will find the latitude and longitude values for the two cities, we will do that using geocoders from geopy. After that we need to use the Foursquare location data to solve the problem. So we need to make a request to Foursquare using our CLIENT_ID and CLIENT_SECRET and the latitude and longitude for each city. The response will be as a json file for ech city and we will get the expected dataframes from the json file using json_normalize. Then we will get a dataframe, from the dataframes of the two cities, consists of name, lat, and long of all hotels in the two cities and we will use this dataframe to get the ceneters of kmeans.

# 3- Solution methodology

First, we get the required data of the two cities from Foursquare, we use CLIENT_ID and CLIENT_SECRET, which we get from Foursquare. The data that we get will be as two json files, one for each city. Then we assign relevant part of JSON to venues and tranform venues into dataframes. Then we do some preprocessing for the cities dataframes to get the required columns. We will get 9 hotels in Aleppo and 3 hotels in Damascus. Then we will show the map that includes the hotels and the center of each city. The center location of the map will be the mean of the locations of the two cities. 

The map that we get is shown below. 

![alt text](https://github.com/baderrasheed/Coursera_Capstone/blob/master/Capture.PNG) 

Then we join the two dataframes in one dataframe. The city isn't shown in the dataframe.
Then we will cluster the hotels into two clusters using KMeans. First we drop 'name' and 'categories' columns and keep just columns tgat help us to make clustering: name , lat, and lng. Obviosly the center of each cluster will be in one city different from the other. This will be just an experiment. In real life, there will be more than two cities, and there may be some hotels out of the cities. KMeans helps to solve these problems.
Then we will show a map with different colors for different clusters or hotels in different clusters. 

The map that we get is shown below. 

![alt text](https://github.com/baderrasheed/Coursera_Capstone/blob/master/Capture1.PNG) 

