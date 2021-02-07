import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    # get the name of the city they're interested in as a string
    # convert to lower case and strip white space so that it's in the same format as the names of
    # the cities in our files
    city = str(input('Which city would you like to analyse? Your options are "chicago", "new york city", and "washington". \n')).lower().strip()

    # make sure the city name has been entered correctly
    city_complete = False
    while city_complete == False:
        if city in ['chicago', 'new york city', 'washington']:
            print('Great! We\'ll show you data from {}.'.format(city.title()))
            break
        else:
            print('Oops! Looks like you made a mistake typing the name of the city. Please copy and paste one of "chicago", "new york city", or "washington".')
            city = str(input('Enter the city you\'d like to analsye here. \n')).lower().strip()
            city_complete = False


    # get user input for month (all, january, february, ... , june)
    # same approach as for city
    month = str(input('Which month are you interested in? Please enter a month from January to June inclusive (write the full name of the month in text), or "all" if want to see data for all the months. \n'))

    month_complete = False
    while month_complete == False:
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            if month != 'all':
                print('Great! We\'ll show you data from {}.'.format(month.title()))
            else:
                print('Great! We\'ll show you data from all months.')

            break
        else:
            print('Oops! Looks like you made a mistake typing the name of the month. Please copy and paste one of "All", "January", "February", "March", "April", "May", or "June".')
            month = str(input('Enter the month you\'d like to analsye here. \n')).lower().strip()
            month_complete = False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # same approach as above
    day = str(input('Which day are you interested in? Please enter the full name of the day in text, or "all" if you\'d like to see data from all the days. \n' ))

    day_complete = False
    while day_complete == False:
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            if day != 'all':
                print('Great! We\'ll show you data from {}.'.format(day.title()))
            else:
                print('Great! We\'ll show you data from all days of the week.')

            break
        else:
            print('Oops! Looks like you made a mistake typing the day. Please copy and paste one of "All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", or "Sunday".')
            day = str(input('Enter the day you\'d like to analsye here. \n')).lower().strip()
            day_complete = False

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load the data for specified city
    df = pd.read_csv(CITY_DATA.get(city))

    # convert Start Time and End Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # create new variables to capture month and day of week that journeys start
    # datetime module is good for this
    df['Month'] = df['Start Time'].dt.month
    # use dt.weekday to get day of week, where Monday is 0 and Sunday is 6.
    df['Day'] = df['Start Time'].dt.weekday

    # now filter by month
    if month != 'all':
        # convert month variable from text to integer to match how it's recorded in df
        # note that we have to add 1 because dt.month returns 1 for january
        month = ["january", "february", "march", "april", "may", "june"].index(month)+1
        df = df[df['Month'] == month]

    # now filter by day
    if day != 'all':
        # convert month variable from text to integer to match how it's recorded in df
        # note that we don't add 1 here because days count up from monday = 0
        day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(day)
        df = df[df['Day'] == day]

    return df

# create a helper function to calculate the "most common" stats for the function below
# returns the value of the most common variable and the number of trips in a string that
# can be printed to the terminal
# capitalise indicates whether the variable label should be capitalised in the output (eg if it's month or day)
# defaults to False
# var_name should be passed as a string
def most_common(df, var_name, text_string):
    highest = df[var_name].mode()[0]
    n_trips = df.groupby([var_name]).size().max()

    # update month/day names from integers to strings for useability
    # first create dictionaries to convert back and forth between integer and string values
    month_dict = {1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june"}
    day_dict = {0:"monday", 1:"tuesday", 2:"wednesday", 3:"thursday", 4: "friday", 5:"saturday", 6:"sunday"}

    # now update values using the dictionaries
    # capitalise so it looks nice
    if var_name == 'Month':
        highest = month_dict.get(highest).title()
    elif var_name == 'Day':
        highest = day_dict.get(highest).title()

    output_string = 'The most common {} in the data you\'ve selected was {}, with {} trips'.format(str(text_string), str(highest), str(n_trips))

    return output_string


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # create dictionaries to convert back and forth between integer and string values
    # for month and day
    month_dict = {1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june"}
    day_dict = {0:"monday", 1:"tuesday", 2:"wednesday", 3:"thursday", 4: "friday", 5:"saturday", 6:"sunday"}

    # display the most common month
    # note that if user is already filtering by month, this is not useful
    if month != 'all':
        print('You only have one month in your dataset. If you\'d like to figure out which month is the most popular, select "all" data for month when you\'re filtering!')
    else:
        output = most_common(df = df, var_name = 'Month', text_string = 'month')
        print(output)

    # display the most common day of week
    # note that if user is already filtering by day, this is not useful
    if day != 'all':
        print('You only have one day in your dataset. If you\'d like to figure out which day is the most popular, select "all" data for day of the week when you\'re filtering!')
    else:
        output = most_common(df = df, var_name = 'Day', text_string = 'day')
        print(output)

    # display the most common start hour
    # extract hour of day from Start Time
    df['Hour'] = df['Start Time'].dt.hour
    output = most_common(df = df, var_name = 'Hour', text_string = 'hour')
    print(output)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    output = most_common(df = df, var_name = 'Start Station', text_string = 'station for starting a trip')
    print(output)

    # display most commonly used end station
    output = most_common(df = df, var_name = 'End Station', text_string = 'station for ending a trip')
    print(output)

    # display most frequent combination of start station and end station trip
    # make a new variable that records start station and end station
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
    output = most_common(df = df, var_name = 'start_end', text_string = 'journey')
    print(output)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # note that journey times are in seconds
    # here we convert to days
    days_travel = df['Trip Duration'].sum()/60/60/24
    # round to one decimal place
    days_travel = round(days_travel, 1)
    # print the output
    print('There were {} total days of travel in the data you selected.'.format(days_travel))

    # display mean travel time in minutes
    mean_trip = df['Trip Duration'].mean()/60
    mean_trip = round(mean_trip, 1)
    # print the output
    print('The average travel time for a single trip was {} minutes.'.format(mean_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The table below shows the number of trips for each type of user:\n')
    print(df.groupby('User Type').size())

    # Display counts of gender
    if city == 'washington':
        print('\nGender data is not available for the city you have selected.\n')
    else:
        print('\nThe table below shows the number of trips for each gender:\n')
        print(df.groupby('Gender').size())

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Birth year data is not available for the city you have selected.')
    else:
        early = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]

        print('\nIn the data you\'ve selected, the earliest birth year is {}, the most recent birth year is {}, and the most common birth year is {}.'.format(int(early), int(recent), int(common)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# define function to display raw data in blocks of 5, with user prompted after each block
def raw_data(df):
    i = 0
    message = '\nWould you like to see some raw data from the dataset you\'ve selected? Enter "yes" or "no".\n'
    while True:
        start = input(message)
        if start == 'yes':
            print('\nHere are rows {} to {} of raw data for the dataset you have selected.\n'.format(i+1, i+5)) # note that we use base 1 indexing in the message as this is more intuitive for the user
            print(df.iloc[i:i+5])
            i += 5
            message = '\nWould you like to see more raw data?\n'
            continue
        elif start == 'no':
            print('Ok, thanks for playing!')
            break
        else:
            print('Oops! Looks like you made a typo! Try again!')
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart with new data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
