import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november',
            'december']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday']

#This section requires user input to generate specific data.

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
    city = 0
    while city not in CITY_DATA.keys():
        city = input('Would you like data for "Chicago", "New York City", or "Washington"? ').lower()


        if city.lower() in CITY_DATA.keys():
            print('You selected city ' + city.title() + '.')
            break
        elif city.lower() == 'new york':
            city = 'New York City'.lower()
            print('You selected city ' + city.title() + '.')
            break
        else:
            print("Sorry, that's an invalid entry.")
            print('\nPlease try again.')
            continue




    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
            month = input('Please select a month to see (or type "all" for all months): ').lower()
            if (month.lower() in months) or (month.lower() == 'all'):
                print('You selected ' + month.title() + '.')
                break
            else:
                print("Sorry, that's an invalid entry. Please try again.")
                continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please select a day of the week (or type "all" for all days): ').lower()
        if ( day.lower() in days) or (day.lower() == 'all'):
            print('You selected ' + day.title() + '.')
            break
        else:
            print("Sorry, that's an invalid entry.  Please try again.")
            continue

    print('-'*40)
    return city, month, day

#The following section loads data relative the specified city and applies
#day and month filters, or allows the user to bypass time filters.
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

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        #Select month using index
        month = months.index(month)
        month = months[month].title()


    if day != 'all':
        #Filter by day of week using index
        day = days.index(day)
        day = days[day].title()
        print(day)


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month for rentals was {}.'.format(common_month))

    # TO DO: display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.dayofweek
    day_index = df['day'].mode()[0]
    common_day = days[day_index]
    print('The most common day for rentals was '+common_day.title()+'.')


    # TO DO: display the most common start hour
    formatted_hour = 0
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    if common_hour > 13:
        formatted_hour = str(common_hour - 12) +':00 PM'
    else:
        formatted_hour = str(common_hour) + ':00 AM'

    print('The most common time (hour) for rentals was '+str(formatted_hour)+'.')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most popular start station is:\n{}.'.format(common_start))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most popular end station is:\n{}.'.format(common_end))


    # TO DO: display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most popular trip is:\n{}.'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    n = df['Trip Duration'].sum()

    total_time = str(datetime.timedelta(seconds=int(n)))

    print('Total time traveled by customers was:')
    print('(Shown in days, hh:mm:ss)\n')
    print(total_time)
    print('\n')

    # TO DO: display mean travel time
    avg_trip = df['Trip Duration'].mode()[0]
    timer = str(datetime.timedelta(seconds=int(avg_trip)))


    print('The average trip time in "hh:mm:ss" was:\n')
    print(timer)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)


    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('Count of users (by gender):\n{}'.format(gender))
    except:
        print('Gender column was not disclosed for this data.')


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        youngest = int((df['Birth Year']).max())
        oldest = int((df['Birth Year']).min())
        common = int((df['Birth Year']).mode())
        print('\nEarliest, most recent and most common birth years of recorded users:\n')
        print('Recent:      '+ str(youngest))
        print('Earliest:    '+ str(oldest))
        print('Most common: '+ str(common))
    except:
        print('Birth date data was absent from the column for this data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data != ('no').lower:
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input('Do you with to continue? y/n')
        if view_display == 'n' or view_display == 'no':
            break
        else:
            continue


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
