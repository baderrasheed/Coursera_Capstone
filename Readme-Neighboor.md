# Introduction/Business Problem

# 1- A description of the problem and a discussion of the background

We will recommend the best places to set up offices for a taxi company, trying to start its own business, that provides services to hotel guests.

To achieve a good start for any new business, it is important to accurately define market requirements first. In the taxi office case, most requests may come from foreign people or from people who have a lot of moves and do not have a car.This kind of people often live in hotels. Therefore, it is best to choose the location of the taxi office so that the distance is as low as possible from hotels in the city. 

Since we are not bound by an option, we will choose cities from Syria (as it's my country) to solve this problem. We will choose two cities (Aleppo and Damascus). The two cities will be treated as one place. After that, the system should find the best places for locating two taxi offices. Each of these two places obviously must be in a different city from the other. We want to get this result using K Means, getting centers at an equal distance from hotels in the city.

# 2- A description of the data and how it will be used to solve the problem.

First we will find the latitude and longitude values for the two cities, we will do that using geocoders from geopy. After that we need to use the Foursquare location data to solve the problem. So we need to make a request to Foursquare using our CLIENT_ID and CLIENT_SECRET and the latitude and longitude for each city. The response will be as a json file for ech city and we will get the expected dataframes from the json file using json_normalize. Then we will get a dataframe, from the dataframes of the two cities, consists of name, lat, and long of all hotels in the two cities and we will use this dataframe to get the ceneters of kmeans.
