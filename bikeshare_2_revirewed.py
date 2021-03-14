import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

days_of_week = ['Monday', "Tuesday", "Wednesday", "Thursday", "friday", "Saturday", "Sunday"]


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
    # limiting user input to numbers for all three entries. with a while , try and if else.
    print("Select the city you want to explore it's data:\n"
          "1.Chicago\n"
          "2.New York\n"
          "3.Washington\n"
          "4.Exit")
    print('-' * 38)
    while True:
        try:
            city = int(input('Please enter a valid number:\n'))
        except ValueError:
            city = input('Please enter a valid number:\n')
            continue
        if int(city) in range(1, 5):
            if int(city) == 1:
                city = 'chicago'
            elif int(city) == 2:
                city = 'new york city'
            elif int(city) == 3:
                (city) = 'washington'
            elif int(city) == 4:
                exit(4)
            break

    print('You have picked:', str(city).title())

    # get user input for month (all, january, february, ... , june)
    # limited as before
    print("Select the month you want to explore it's data:\n"
          "1.January\n"
          "2.February\n"
          "3.March\n"
          "4.April\n"
          "5.May\n"
          "6.June\n"
          "7.All\n")
    print('-' * 38)
    while True:
        try:
            month = int(input('Pick month number: \n'))
        except ValueError:
            month = input('Please enter a valid month number:\n')
            continue
        if int(month) in range(1, 8):
            if int(month) == 1:
                month = 'january'
            elif int(month) == 2:
                month = 'february'
            elif int(month) == 3:
                month = 'march'
            elif int(month) == 4:
                month = 'april'
            elif int(month) == 5:
                month = 'may'
            elif int(month) == 6:
                month = 'june'
            elif int(month) == 7:
                month = 'all'
            break
    print('You picked: \n', str(month).title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # more limitation
    print("Select the day you want to explore it's data:\n"
          "1.Monday\n"
          "2.Tuesday\n"
          "3.Wednesday\n"
          "4.Thursday\n"
          "5.Friday\n"
          "6.Saturday\n"
          "7.Sunday\n"
          "8.All")
    print('-' * 38)

    while True:
        try:
            day = int(input('Pick day number:\n'))
        except ValueError:
            day = input('Please enter a valid day number:\n')
        if int(day) in range(1, 9):
            if int(day) == 1:
                day = 'monday'
            elif int(day) == 2:
                day = 'tuesday'
            elif int(day) == 3:
                day = 'wednesday'
            elif int(day) == 4:
                day = 'thursday'
            elif int(day) == 5:
                day = 'friday'
            elif int(day) == 6:
                day = 'saturday'
            elif int(day) == 7:
                day = 'sunday'
            elif int(day) == 8:
                day = 'all'
            break
    print('You have picked:', city.title(), month.title(), day.title())
    print('-'*38)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
                            data , index
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city = CITY_DATA[city]
    # load data file into a dataframe
    df = pd.read_csv(city)
    if 'Gender' in df:
        df['Gender'] = df['Gender'].fillna(value='not specified')
    if 'User Type' in df:
        df['User Type'] = df['User Type'].fillna(value='not available')
    if 'Birth Year' in df:
        df['Birth Year'] = df['Birth Year'].fillna(value=df['Birth Year'].mean())

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day...
    if day != 'all':
        day = days_of_week.index(day.title())
        df = df[df['day_of_week'] == day]
        print(df)

    # some missing data causing errors: search and fill:
    # chicago (gender and birth), not affecting the results,  filled
    # new york(user type, gender , birth) affecting the results, ignored with "if"

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()  # number
    month_list = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november',
                  'december']
    named_common_month = month_list[common_month-1]  # convert to name
    print('The most common month', named_common_month.title(), '\n')

    # display the most common day of week
    print("The most common day of the week", days_of_week[df['day_of_week'].value_counts().idxmax()], '\n')

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    print('most common start hour is:', df['Start Time'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 38)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station']
    print('the most common used start station:', start_station.value_counts().idxmax())

    # display most commonly used end station
    end_station = df['End Station']
    print('the most common used end station:', end_station.value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    start_end_station = df[['Start Station', 'End Station']]
    print('The most frequent combination of start stations and end stations trip:\n ',
          (start_end_station.cummax(axis=1)).head(1))  # pandas version 0.23.4
    # my original answer start_end_station.value_counts().idxmax()  pandas version 1.2.1

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 38)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour   # extracting hour
    df['hour'] = pd.DatetimeIndex(df['End Time']).hour
    # find the most common hour (from 0 to 23)
    # popular_hour = df['hour'].value_counts().idxmax()
    popular_hour = df['hour'].mode()[0]
    # Udacity answer diff than mine , output is the same,but when i submit caused an error there
    # Need to search the diff , causing error in start_end_station
    print('The most popular hour :', popular_hour)
    # display mean travel time
    mean_travel = (df['End Time'] - df['Start Time']).mean()  # can i format and remove milli sec ?
    print('Average time of travel:', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 38)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    if "User Type" in df:
        user_types = df['User Type'].value_counts()
        print(user_types)

    # Display counts of gender
    if "Gender" in df:
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        dob = df['Birth Year']
        print('the oldest user birthdate:', dob.min())
        print('the youngest user birthdate:', dob.max())
        print('the most common birthdate:', dob.value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 38)


def descriptive_statistics():
    while True:
        try:
            confirm = int(input('Do you want to check the data files? Pick a number.:\n'
                                '1.Yes\n'
                                '2.No, Restart.\n'
                                '3.No, Exit\n'))
        except ValueError:
            confirm = input('Please enter a valid number:\n')
            continue
        if int(confirm) in range(1, 4):
            if int(confirm) == 1:
                raw_data()
            elif int(confirm) == 2:
                main()
            elif int(confirm) == 3:
                exit(3)
            break


def raw_data():
    print('Lets check some data!')
    print("-" * 38)
    while True:
        try:
            city = int(input("Great, Which city you want to check? Pick a number:\n"
                             "1.Chicago.\n"
                             "2.New York.\n"
                             "3.Washington\n"
                             "4.Restart\n"
                             "5.Exit\n"))
            print('-' * 38)
        except ValueError:
            city = int("Enter a valid number: \n")
            continue

        if int(city) == 1:
            city = CITY_DATA['chicago']
        elif int(city) == 2:
            city = CITY_DATA['new york city']
        elif int(city) == 3:
            city = CITY_DATA['washington']
        df = pd.read_csv(city)
        print(df.describe())
        print(df.info())
        print(df.head(21))
        print(df.columns)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        descriptive_statistics()


if __name__ == "__main__":
    main()
