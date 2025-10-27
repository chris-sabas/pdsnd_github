import time
import pandas as pd
import numpy as np

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
    city = input("Please enter the city you want to explore (chicago, new york city, washington): ").lower()
    while city not in CITY_DATA:    
        print("Invalid input. Please try again.")
        city = input("Please enter the city you want to explore (chicago, new york city, washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter the month you want to explore (all, january, february, ... , june): ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print("Invalid input. Please try again.")
        month = input("Please enter the month you want to explore (all, january, february, ... , june): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day of week you want to explore (all, monday, tuesday, ... , sunday): ").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print("Invalid input. Please try again.")
        day = input("Please enter the day of week you want to explore (all, monday, tuesday, ... , sunday): ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable. Shows raw data if requested.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # ask if the user wants to see raw data
    show_raw_data = input("\nWould you like to see the first 5 rows of raw data? Enter yes or no: ").lower()
    
    # show the first 5 rows of raw data if the user wants to see it and ask if more rows should be shown
    i = 0
    while show_raw_data == 'yes' and i < len(df):
        print(df.iloc[i:i+5])
        i += 5
        show_raw_data = input("Would you like to see the next 5 rows of raw data? Enter yes or no: ").lower()
    print('-'*40)

    # convert the 'Start Time' and 'End Time' columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from 'Start Time' to create a new column (used later)
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month:", df['month'].mode()[0])

    # display the most common day of week
    print("Most common day of week:", df['day_of_week'].mode()[0])

    # display the most common start hour
    print("Most common start hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station:", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most commonly used end station:", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip:",
          (df['Start Station'] + " to " + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).dt.total_seconds()
    print("Total travel time:", total_travel_time.sum(), "seconds")

    # display mean travel time
    print("Mean travel time:", total_travel_time.mean(), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print("No gender data available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest year of birth:", df['Birth Year'].min())
        print("Most recent year of birth:", df['Birth Year'].max())
        print("Most common year of birth:", df['Birth Year'].mode()[0])
    else:
        print("No birth year data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def confirm_filters(city, month, day):
    """
    Confirms the filters applied by the user.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (bool) True if the user confirms the filters, False if they want to restart
    """
    print(f"\nYou have chosen to explore data for {city.title()} in {month.title()} during {day.title()}.")
    print("If this is correct, press Enter to continue or type 'no' to restart.")
    
    # Get user confimation, if 'no' is entered, return False
    if input().lower() == 'no':
        print('-'*40)
        return False
    print('-'*40)
    return True


def main():
    while True:
        # Get user input for city, month, and day
        city, month, day = get_filters()

        # Confirm filters with the user
        if not confirm_filters(city, month, day):
            continue
        
        # Load data and output raw data if requested
        df = load_data(city, month, day)

        # Perform analysis
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Aask if the user wants to restart the program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()