import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def yes_or_no(phrase):
    """
    Asks user to choose yes or no.

    Returns:
        (str) choice - yes or no
    """
    while True:
        choice = input(phrase)
        if choice.lower() in ['yes', 'no']:
            break
        else:
            print('Invalid choice! Please type "Yes" or "No".')
    return choice.lower()


def print_first_5_lines(df):
    """
    Print the first lines from raw data.
    """
    choice = yes_or_no('Do you want to see 5 lines of raw data? (Yes / No)\n')
    if choice == 'yes':
        print('\nShowing first 5 lines of raw data:\n')
        print(df.head(5))
        input('Press enter to continue...')
    print('Starting statistics calculations...\n')
    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input("\nWould you like to see data for Chicago, New York, or  Washington?\n").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid city name! Please choose one of the 3 cities.")

    # get user input for month (all, january, february, ... , june)
    choice = yes_or_no('\nWould you like to filter the data by month? (Yes / No)\n')    
    if choice == 'yes':        
        while True:
            month = input("\nWhich month? January, February, March, April, May or June? Please type out the full month name.\n").title()
            if month in months:
                break
            else:
                print("Invalid month! Please choose one of the months listed.")
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)

    choice = yes_or_no('\nWould you like to filter the data by weekday? (Yes / No)\n')
    if choice == 'yes':
        while True:
            day = input("\nWhich day? Please type out the full weekday name.\n").title()
            if day in weekdays:
                break
            else:
                print("Invalid day! Please choose one of the weekdays.")
    else:
        day = 'all'

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    #print(df['month'])
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #print(df['day_of_week'])

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('What is the most popular month for travelling?')
    most_common_month = df['month'].value_counts().index[0]
    print(most_common_month)

    # display the most common day of week
    print('\nWhat is the most popular day of week for travelling?')
    most_common_weekday = df['day_of_week'].value_counts().index[0]
    print(most_common_weekday)

    # display the most common start hour
    print('\nWhat is the most popular hour of day to start the travels?')
    start_hour = df['Start Time'].dt.hour.value_counts().index[0]
    print(start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nWhat is the most popular start station?')
    popular_start_station = df['Start Station'].value_counts().index[0]
    print(popular_start_station)

    # display most commonly used end station
    print('\nWhat is the most popular end station?')
    popular_end_station = df['End Station'].value_counts().index[0]
    print(popular_end_station)

    # display most frequent combination of start station and end station trip
    print('\nWhat is the most trip from start to end?')
    df['COUNTER'] = 1 # add the column 'COUNTER' with all cells with value 1
    most_popular_trip = df.groupby(['Start Station','End Station'])['COUNTER'].sum().nlargest(1)
    print(most_popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('What is total duration of all trips?')
    total_travel_time = df['Trip Duration'].sum()
    hours = total_travel_time // 3600
    minutes = (total_travel_time - hours*3600) // 60
    if (hours > 23):
        days = hours // 24
        hours = hours % 24
        print(f'{days} days, {hours} hours and {minutes} minutes')
    else: 
        print(f'{hours} hours and {minutes} minutes') 

    # display mean travel time
    print('\nWhat is mean duration of all trips?')
    mean_duration = df['Trip Duration'].mean()
    minutes = mean_duration // 60
    seconds = mean_duration - minutes*60
    print(f'{minutes:0.0f} minutes and {seconds:0.0f} seconds')    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('How many user per type?')
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender

    if "Gender" in df.columns:
        print('\nHow many user per gender?')
        users_per_gender = df['Gender'].value_counts()
        print(users_per_gender)

    # Display earliest, most recent, and most common year of birth

    # Check if "Birth Year" is available
    if "Birth Year" in df.columns:
        print('\nWhat is the oldest, youngest and the most popular birth of year, respectively?')
        newest_birth_year = df['Birth Year'].min()
        oldest_birth_year = df['Birth Year'].max()
        most_commom_birth_year = df['Birth Year'].value_counts().index[0]
        print(f'{newest_birth_year}, {oldest_birth_year} and {most_commom_birth_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print('Just a moment... loading data...\n')
        df = load_data(city, month, day)
        print('Data loaded.\n')
        print_first_5_lines(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
