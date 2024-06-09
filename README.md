# sqlalchemy-challenge
# Part 1: climate_starter.ipynb
There were some spots were I needed the AI assitant to get me through this challenge. The first instance was for the list comprehension to get the dataframe:   
    data = [{"Date": date, "Preciptation(Inches)": prcp} for date, prcp in twelve_month_prcp]
I was also having some trouble with the format of my bar chart, as the graph was coming out really small because the dares were all smushed together on the xaxis.
I used this command that was given to me by the AI assitant to narrow the dates down to 6 so the graph looks nicer: 
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(6))
Finally, I needed help with another list comprehension to get the station ids and counts for each station:
    station_id_counts = [(station, count) for station, count in station_count]

# Part 2: Flask app
Similar to part 1 there were instances I needed help with creating a list of dictionaries for the queried data in which I used the AI assitant for:
    95. temps_list = [{"date": date, "tobs": tobs} for date, tobs in twelve_month_temp]. 
        For this one I tried to run the app with just date:tobs and was getting an error. The AI told me to add those keys and it worked.
    109. start_list = [{"TMIN": query[0], "TAVG": query[1], "TMAX": query[2]} for query in start_query]
    124.  start_end_list = [{"TMIN": query[0], "TAVG": query[1], "TMAX": query[2]} for query in stats_query]
        For these two, I was struggling with getting the results into a list of dictionaries. What I did wrong was forgetting to add [0],[1],[2] since the results off the max,min,avg were queried into a string.
