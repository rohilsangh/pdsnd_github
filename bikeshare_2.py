import time
import pandas as pd
import numpy as np
import os 


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# dictionary of days of the week from id to name
days_of_the_week = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

months_of_the_year = {
    1: 'January',
    2: 'Feburay',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

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
    city_inputvalid = False
    while city_inputvalid == False:
        city = input('Would you like to see data for Chicago, New York City, or Washington?')
        city = city.lower()
        if city not in list(CITY_DATA.keys()):
            print('Invalid input, please try again.')
        else:
            city_inputvalid = True
    
    # filter by what kind of data the user selects
    valid_filter = False
    while valid_filter == False:
        filter_type = input('Would you like to filter the data by month, day, or not at all? (day, month or none)')
        filter_type = filter_type.lower()
        if filter_type not in ['day', 'month', 'none']:
            print('Invalid input, please try again')
        else:
            valid_filter = True

    if filter_type == 'month':    
        # get user input for month (all, january, february, ... , june)
        month = input('What month number (e.g. 3 is March)?')
    else:
        month = None

    if filter_type == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Which day? (Monday = 0, Wednesday = 2)')
    else:
        day = None

    print('-'*40)
    return city, filter_type, month, day


def load_data(city, filter_type, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        loaded_data - all data for given city
        filtered_df (df) - DataFrame containing city data filtered by month and day
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    loaded_data = pd.read_csv(dir_path+'\\'+ CITY_DATA[city])

    loaded_data['start_time_dt'] = pd.to_datetime(loaded_data['Start Time'])
    loaded_data['start_month'] = [i.month for i in loaded_data['start_time_dt']]
    loaded_data['start_day'] = [i.weekday() for i in loaded_data['start_time_dt']]
    loaded_data['start_hour'] = [i.hour for i in loaded_data['start_time_dt']]

    if filter_type == 'none':
        filtered_df = loaded_data
    elif filter_type == 'month':
        month = int(month)
        filtered_df = loaded_data[loaded_data['start_month'] == month]
    elif filter_type == 'day':
        day = int(day)
        filtered_df = loaded_data[loaded_data['start_day'] == day]

    return loaded_data, filtered_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df.start_month.mode().iloc[0]
    print('Most common month: ', months_of_the_year[most_common_month])

    # display the most common day of week
    most_common_day = df.start_day.mode().iloc[0]
    print('Most common day: ', days_of_the_week[most_common_day])

    # display the most common start hour
    most_common_hour = df.start_hour.mode().iloc[0]
    print('Most common start hour: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start = df['Start Station'].mode().iloc[0]
    print('Most commonly used start station: ', mode_start)

    # display most commonly used end station
    mode_end = df['Start Station'].mode().iloc[0]
    print('Most commonly used end station: ', mode_end)

    # display most frequent combination of start station and end station trip
    most_f_combo = (df['Start Station'] + ' to ' + df['End Station']).mode()
    print('Most common Start- End Station combination: ', most_f_combo.iloc[0])

    # timer to monitor how long this function has taken to execute
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time (mins): ', df['Trip Duration'].sum())

    # display mean travel time
    print('Average travel time (mins): ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type Counts: ', df['User Type'].value_counts())

    # try except used to deal with any exceptions and errors in dataset
    try:
        # Display counts of gender
        print('Gender Counts: ', df['Gender'].value_counts())
        
        # Display earliest, most recent, and most common year of birth
        # earliest
        print('Earliest birth year: ', int(df['Birth Year'].min()))

        # most recent
        print('Most Recent birth year: ', int(df['Birth Year'].max()))

        # most common
        print('Most common birth year: ', int(df['Birth Year'].mode().iloc[0]))
    
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(data_df):
    '''
    Upon user input displays 5 rows at a time of data.
    '''
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    user_continue = True
    
    while user_continue:
        print(data_df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_input = True
        while view_input:
            view_data = input("Do you wish to continue? (y for yes, n for no): ").lower()
            if view_data == 'y':
                view_input = False
                continue
            elif view_data == 'n':
                user_continue = False
                view_input = False
                continue
            else:
                print('Invalid Input, please try again')


def main():
    while True:
        city, filter_type, month, day = get_filters()
        all_df, filtered_df = load_data(city, filter_type, month, day)

        time_stats(filtered_df)
        station_stats(filtered_df)
        trip_duration_stats(filtered_df)
        user_stats(filtered_df)
        display_data(filtered_df)

        restart_input_valid = True
        while restart_input_valid:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart in ['yes', 'no']:
                restart_input_valid = False
            else:
                print('Please enter valid input')
        if restart.lower() != 'yes':
            break 

if __name__ == "__main__":
	main()

