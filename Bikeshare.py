import time
import pandas as pd


city_data = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    cities = ['Chicago', 'New York City', 'Washington']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All']
    print('Hello! Let\'s explore some US Bikeshare data!')

    city = input('Please choose one of the following cities (Chicago, New York City, Washington):')
    while city.title() not in cities:
        city = input('Please make sure your input is one of the following cities (Chicago, New York City, Washington):')

    month = input('Please choose one of the following months or choose All to explore data for all months\
 (January, February, March, April, May, June, All):')
    while month.title() not in months:
        month = input('Please make sure your input is one of the following months or All to explore data for all months\
 (January, February, March, April, May, June, All):')

    day = input('Please choose one of the following days or choose All to explore data for all days\
 (Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All):')
    while day.title() not in days:
        day = input('Please make sure your input is one of following days or All to explore data for all days\
 (Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All):')

    print('\nyou have chosen the following inputs for data lookup: {}, {}, {}\n'.format(city, month, day).title())
    print('Please wait while we fetch the needed data...')
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(city_data[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    df['hour'] = df['Start Time'].dt.hour

    if month.title() != 'All':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]

    if day.title() != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    print('\n*** The Most Frequent Times of Travel ***\n')
    start_time = time.time()
    if month.title() == 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        common_month = df['month'].mode()[0]
        print('The most common month is {}'.format(months[common_month-1]))

    if day.title() == 'All':
        common_day = df['day_of_week'].mode()[0]
        print('The most common day is {}'.format(common_day))

    common_hour = df['hour'].mode()[0]
    print('The most common start hour is {}:00'.format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\n*** The Most Popular Stations and Trip ***\n')
    start_time = time.time()
    common_start = df['Start Station'].mode()[0]
    common_end = df['End Station'].mode()[0]
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print('The most common start station is {}'.format(common_start))
    print('The most common end station is {}'.format(common_end))
    print('The most common trip is {}\n'.format(common_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def duration_stats(df):
    print('\n*** Trip Duration Calculation ***\n')
    start_time = time.time()
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()
    print('The total travel duration is {} seconds'.format(total_duration))
    print('The mean travel duration is {} seconds\n'.format(mean_duration))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    print('\n*** User Related Stats ***\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print('\nUser Types Count:\n')
    print(user_types)
    if city.title() != 'Washington':
        user_gender = df['Gender'].value_counts()
        birth_young = df['Birth Year'].max()
        birth_old = df['Birth Year'].min()
        birth_common = df['Birth Year'].mode()[0]
        print('\nUser Gender Count:\n')
        print(user_gender)
        print('\nThe earliest year of birth is {}'.format(birth_old))
        print('The most recent year of birth is {}'.format(birth_young))
        print('The most common year of birth is {}\n'.format(birth_common))
    elif city.title() == 'Washington':
        print('\nUnfortunately, Gender and birth year data are not available for this city.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(city):
    df = pd.read_csv(city_data[city.lower()])
    print('\n*** Raw data is ready for display ***\n')
    start_point = 0
    while True:
        choice = input('Would you like to display the raw data? (Yes/No):')
        if choice.title() not in ['Yes', 'No']:
            print('Please make sure your input is Yes or No')
        elif choice.title() == 'Yes':
            print(df.iloc[start_point:start_point+5])
            start_point += 5
        elif choice.title() == 'No':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        duration_stats(df)
        user_stats(df, city)
        raw_data(city)
        restart = input('\nWould you like to restart? (Yes/No):')
        if restart.lower() != 'yes':
            print('\n*** Thank you for using the US Bikeshare statistics application ***')
            break


if __name__ == "__main__":
    main()
