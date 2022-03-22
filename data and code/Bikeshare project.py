import pandas as pd
import time
import numpy as np

CITY_DATA = {'c': "chicago.csv", 'n': "new_york_city.csv", 'w': "washington.csv"}


def get_filters():
    city_selection = input(
        "Kindly select a city to display statistics about. You can type (n) for new york city, (w) for washington, or (c) for chicago : ").lower()
    while city_selection not in ['n', 'c', 'w']:
        print("that's invalid input")
        city_selection = input(
            "Kindly select a city to display statistics about. You can type (n) for new york city, (w) for washington, or (c) for chicago : ").lower()

    months = ["january", "february", "march", "april", "may", "june", "all"]
    month = input("please Enter the month :\njanuary\nfebruary\nmarch\napril\nmay\njune\nall for all months\n").lower()
    while month not in months:
        print("that's invalid input")
        month = input(
            "please Enter the month :\njanuary\nfebruary\nmarch\napril\nmay\njune\nall for all months\n").lower()

    days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"]
    day = input("Which day - sunday, monday, tuesday, wednesday, thursday, friday, saturday or all?").lower()
    while day not in days:
        print("that's invalid input")
        day = input("Which day - sunday, monday, tuesday, wednesday, thursday, friday, saturday or all?").lower()

    print('-' * 40)
    return city_selection, month, day


def load_data(city, month, day):
    # read the dataframe using the city
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    if month == 'all':
        popular_month = df['month'].mode()[0]
        months = ["january", "february", "march", "april", "may", "june"]
        popular_month = months[popular_month - 1]
        print('Most Frequent Month:', popular_month)

    # display the most common day of week
    if day == 'all':
        popular_weekday = df['day_of_week'].mode()[0]
        print('Most Frequent Weekday:', popular_weekday)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_start_station = df['Start Station'].mode()[0]
    print("\nThe most start station: ")
    print(most_start_station)

    most_end_station = df['End Station'].mode()[0]
    print("\nThe most end station: ")
    print(most_end_station)

    # display most frequent combination of start station and end station trip
    df['rout'] = df['Start Station'] + " - " + df['End Station']
    print("\nThe most frequent combination of start station and end station trip: ")
    print(df['rout'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("\nThe total travel time in seconds: ")
    print(total_time)

    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print("\nThe average travel time in seconds: ")
    print(average_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print("\nThe count of each user type: ")
    print(user_types)

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts().to_frame()
        print("\nThe count of each user gender: ")
        print(user_gender)
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print("\nThe earliest year of birth: ")
        print(int(earliest_birth))

        recent_birth = df['Birth Year'].max()
        print("\nThe recent year of birth: ")
        print(int(recent_birth))

        common_birth = df['Birth Year'].mode()[0]
        print("\nThe common year of birth: ")
        print(int(common_birth))
    except KeyError:
        print("\nThis data (Gender and Birth Year) is not available for Washington")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(city):
    print("\nRaw data is available to check...\n")
    display_raw=input("Do you want to have a look on the raw data (display 5 rows) ? type (y) for yes or (n) for no: \n")
    while display_raw not in['y','n']:
        print("Invalid input please re-enter your selection again..")
        display_raw = input("Do you want to have a look on the raw data ? type (y) for yes or (n) for no: \n")
    while display_raw=='y':
        try:
            for chunk in pd.read_csv(CITY_DATA[city] ,chunksize=5):
                print(chunk)
                display_raw = input("Do you want to have another look on the raw data (display 5 rows)  ? type (y) for yes or (n) for no: \n")
                if display_raw !='y':
                    print("Thank you")
                    break
            break
        except KeyboardInterrupt:
            print("Thank you")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)

        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()



