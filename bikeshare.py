# bikeshare project
# Mark Waltz

import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']


def get_city():
    """
    Asks user to input a city. The city must be either Chicago, New York City
    or Washington.

    Returns:
        (str) city_entered - name of the city to analyze in lower case.
    """

    while True:
        city_entered = input("\nWould you like to see data for Chicago, New York or Washington? ").lower()

        if city_entered in CITY_DATA.keys():
            return city_entered
        else:
            print("Chicago, New York or Washington only, please.... ")


def get_additional_filtering():
    """
    Asks user whether additional filtering (by month, day, both or none) is
    desired.

    Returns:
        (str) additional_filter: "month", "day", "both" or "none".
    """
    addl_filters = ['month', 'day', 'both', 'none']

    while True:
        filter_entered = input("\nWould you like to filter the data by month, day, both or none at all? ").lower()

        if filter_entered in addl_filters:
            return filter_entered
        else:
            print("Month, day, both or none only, please.... ")


def get_month():
    """
    Asks user to input a month name or "all" (case insensitive). The month, if
    provided, must fall between January and June.

    Returns:
        (str) month_entered - "all" or name of the month in lower case.
    """

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month_entered = input("\nWhich month - January, February, March, April, May or June? ").lower()

        if month_entered in months:
            return month_entered
        else:
            print("Any month between January and June (inclusive), or 'all' if you've changed your mind, please.... ")


def get_day():
    """
    Asks user to input a day name or "all" (case insensitive).

    Returns:
        (str) day_entered - "all" or name of the day in lower case.
    """

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day_entered = input(
            "\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ").lower()

        if day_entered in days:
            return day_entered
        else:
            print("Only a day name (Monday, Tuesday, etc) or 'all' if you've changed your mind, please.... ")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data! ")

    city = ''
    month = 'all'
    day = 'all'

    try:
        # get user input for city (chicago, new york city, washington).
        city = get_city()
        addl_filtering = get_additional_filtering()

        if addl_filtering == 'both':
            month = get_month()
            day = get_day()
        elif addl_filtering == 'month':
            month = get_month()
        elif addl_filtering == 'day':
            day = get_day()

    except KeyboardInterrupt:
        print("\n\nYou have requested that we quit! ")
        quit()

    print('-' * 40)
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

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
    common_month = df['month'].mode()[0]
    print('Most Common Month: ', MONTHS[common_month - 1].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("Most Common Day of Week: ", common_day)

    # display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most Common Start Hour: ", common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: ", common_end_station)

    # display most frequent combination of start station and end station trip from
    # https://stackoverflow.com/questions/19384532/how-to-count-number-of-rows-per-group-and-other-statistics-in
    # -pandas-group-by This works, but I don't think I really understand why... this took a LONG TIME to figure
    # out!!!! More in-depth instruction on this would have been helpful.

    freq = df.groupby(['Start Station', 'End Station'])['Start Time'].count().sort_values(ascending=False)

    print("\nMost Frequent Start/Stop Station Combination: ")
    print("    Start station:", str(freq.index[0][0]))
    print("    End station:", str(freq.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print("User Types Counts:\n ", user_types_counts)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("\nGender Counts: \n", gender_counts)
    except:
        print("Gender counts are not currently available for", city.title())

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birthday = df['Birth Year'].min()
        print("Year of Birth: Earliest:", earliest_birthday)

        most_recent_birthday = df['Birth Year'].max()
        print("Year of Birth: Most Recent:", most_recent_birthday)

        most_common_birthday = df['Birth Year'].mode()[0]
        print("Year of Birth: Most Common:", most_common_birthday)
    except:
        print("Birth Year statistics are not currently available for", city.title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    """
     Asks user if viewing the raw data is wanted.  Displays data five rows at a time until a non-'y'
     prompt response.

     """
    rows_shown = 5
    start = 0
    stop = rows_shown
    while True:
        see_raw_data = input("\nWould you like to see raw data? ").lower()

        if see_raw_data == 'y' or see_data == 'yes':
            print(df[start:stop])
            start += rows_shown
            stop += rows_shown
        else:
            return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
