import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = { 'January': 1, 'February': 2,
               'March': 3, 'April': 4,
               'May': 5, 'June': 6}

DAY_DATA = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6}

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

    city = ''
    while city not in CITY_DATA:
        city = input('\nPlease enter the city you wish to see data for: Chicago, New York City, or Washington? ').lower()
        if city not in CITY_DATA:
            print('You have entered an invalid city, namely:', city, '  Please try again.\nOr if you do not wish to proceed then please exit the program')

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in MONTH_DATA and month != 'All':
        month = input('\nPlease enter the month: January, February, March, April, May or June\nOr enter \'all\' for all months: ').title()
        if month not in MONTH_DATA and month != 'All':
            print('You have entered an incorrect value, namely:', month, '  Please try again.\nOr if you do not wish to proceed then please exit the program')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in DAY_DATA and day!= 'All':
        day = input('\nPlease enter the day of the week (e.g. Monday, Tuesday ...), or \'all\' for all data: ').title()
        if day not in DAY_DATA and day!= 'All':
            print('You have entered an incorrect value, namely:', day, '  Please try again.\nOr if you do not wish to proceed then please exit the program')

    #print(city, month, day)
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
    dfmonth = 'All'
    dfday = 'All'

    df = pd.read_csv(CITY_DATA[city])  # Open relevant data file
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month # Create new column 'Month'
    df['WeekDay'] = pd.to_datetime(df['Start Time']).dt.dayofweek   # Create new column 'WeekDay'

    if month != 'All':
        dfmonth = MONTH_DATA[month] # take integer equivalent of month

    if day != 'All':
        dfday = DAY_DATA[day] # take integer of weekday

    if month == 'All':
        if day != 'All':  #Filter by all months and the day of the week

            df = df[(df['WeekDay'] == dfday)]  # Filter data by weekday

    else:
        if day == 'All':   # Filter by month only
            df = df[(df['Month'] == dfmonth)]  # Filter data by month
        else:     # Filter by month and by week day entered
            df = df[(df['Month'] == dfmonth) & (df['WeekDay'] == dfday)]  # Filter data by month and day of week

    return df


def display_data(df):
    """
       Displays data 5 lines at a time from the prepared DataFrame - (df)
       It will keep displaying data until the user enters 'no'
    """
    print('\n\n')
    view_data = ''
    while view_data != 'yes' and view_data != 'no':
        view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no? ').lower()
        if view_data != 'yes' and view_data != 'no':
            print('Incorrect value entered: ', view_data)
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = ''
        while view_data != 'yes' and view_data != 'no':
            view_data = input("Do you wish to continue? Please enter yes or no: ").lower()
            if view_data != 'yes' and view_data != 'no':
                print('Incorrect value entered: ', view_data)
    print('\n\n')

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    DY_DATA = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday', 6: 'Sunday' }

    MTH_DATA = { 1: 'January', 2: 'February',
                 3: 'March', 4: 'April',
                 5: 'May', 6: 'June' }



    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]

    print('\nThe most common month to travel is: ', MTH_DATA[common_month])

    # display the most common day of week
    common_weekday = df['WeekDay'].mode()[0]
    print('\nThe most common day of the week to travel is: ', DY_DATA[common_weekday])

    # display the most common start hour
    #pd.to_datetime(df['Start Time']).dt.month
    common_hour = pd.to_datetime(df['Start Time']).dt.hour.mode()[0]

    print('\nThe most common start hour is: ', common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startstation = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is: ', common_startstation)

    # display most commonly used end station
    common_endstation = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is: ', common_endstation)

    # display most frequent combination of start station and end station trip
    df['StartEndStation'] = df['Start Station'] + df['End Station']

    print('\nThe most frequent combination of start station and end station trip is:\n', df['StartEndStation'].mode()[0])
    #print(frequent_stationcomb)
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal Travel Time was: ', df['Trip Duration'].sum())

    # display mean travel time
    print('\nMean Travel Time was: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    df
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\n\nDisplay counts of user types\n')
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\n\nDisplay Gender counts\n')
        print(df['Gender'].value_counts())
    else:
        print('\nThere is no Gender data\n')

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        print('\n\nDisplaying Birth Year information ...\n\n')
        print('\nThe earliest Birth Year is: ', int(df['Birth Year'].min()))
        print('\nThe most recent Birth Year is: ',int(df['Birth Year'].max()))
        print('\nThe most common Birth Year is: ',int(df['Birth Year'].mode()))
    else:
        print('\nThere is no Birth Year data\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
