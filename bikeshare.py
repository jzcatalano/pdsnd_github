import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

city_names = ('chicago', 'new york city', 'washington')
# by listing month names with all first then the remaining month names each have an index value equal to their month number on a calendar
month_names = ('all', 'january', 'february', 'march', 'april', 'may', 'june')

day_names = ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while (True):
        city = input("Enter a city name from this list (i.e., Chicago, New York City, or Washington):  ")
        if city.lower() in city_names:
            break
    #using the lower() allows all use input to be evaluated based on the lowercase spelling of the words and accounting for a mix of uppercase and lowercase characters entered by the user
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while (True):
        month = input("Enter the name of the month you want to analyze (from January through June). Or write 'all' to not filter by month.  ")
        if month.lower() in month_names:
            break
        else:
            print ('Try again - Select a valid month from January to June. Or write all to not filer by month.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while (True):
        day = input("Enter the day of the week that you want to analyze. Or write 'all' to not filter by day. ")
        if day.lower() in day_names:
            break

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
    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # convert month name to month number
    month_number = month_names.index(month.lower())

    # filter by month to create the new dataframe
    if month_number > 0:
        df = df[df['month'] == month_number]

    # filter by day of week to create the new dataframe
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = month_names[df['month'].mode()[0]].title()
    print('Most Popular Month:  ', popular_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:  ', common_day)

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_start_hour = df['start_hour'].mode()[0]
    print('Most Common Start Hour:  ', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:  ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:  ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_and_End_Stations'] = 'Start Station: ' + df['Start Station'] + ' and End Station: ' + df['End Station']
    common_combo = df['Start_and_End_Stations'].mode()[0]
    print('The most frequent combination of start station and end station is:  \n', common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time for all users was ', total_travel_time, 'seconds.')
    print('\nThe total travel time for all users was ', total_travel_time / 60, 'minutes.')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time was ', int(mean_travel_time), 'seconds.')
    print('\nThe mean travel time was ', int(mean_travel_time) / 60, 'minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print(user_types)
    else:
        print('There is no User Type data for this city.')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print('\nThere is no Gender data available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_earliest = df['Birth Year'].min()
        birth_year_most_recent = df['Birth Year'].max()
        birth_year_common = df['Birth Year'].mode()[0]
        print('The earliest birth year is: ', int(birth_year_earliest), '\nThe most recent birth year is: ', int(birth_year_most_recent), '\nThe most common birth year is: ', int(birth_year_common))
    else:
        print('\nThere is no birth year information available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    """Asks user if they want to see the first five rows of data. Then continually ask if the user wants five more rows."""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc : (start_loc+5)])
        start_loc += 5
        view_data = input("Do you wish to see 5 more rows of data? Enter yes or no.\n").lower()
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
