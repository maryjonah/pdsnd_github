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
    print('Hello lovely user! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input("Select a city: 'Chicago', 'New York City', 'Washington':\n")
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("There is no data for this city, please choose between Chicago, New York City or Washington")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Type a month between January and June (write out in full) or all:\n")

        if month.lower() not in ('january','february','march','april','may','june', 'all'):
            print('There is no data for this month, please any month between January and June')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter a day between Monday and Sunday or type all: \n")
        if day.lower() not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'all'):
            print('Incorrect day, please spell the day correctly in full')        
        else:
            break

    city, month, day = city.lower(), month.lower(), day.lower()
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
    
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
       # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    else:
        df = df

    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    else:
        df = df

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
        
    # display the most common month
    popular_hour = df['month'].mode()[0]
    print('Popular Hour: ' + str(popular_hour))

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('Popular day of week: ' + str(popular_dow))

    # display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('Popular Start Hour: ' + str(popular_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Popular Start Station: {}'.format(popular_start_station))
    print('Popular End Station: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_start_end_stations = (df.groupby(['Start Station', 'End Station']).size() 
                                    .sort_values(ascending=False) 
                                    .reset_index(name='count'))

    
    print("\nPOPULAR STATION WHERE CLIENTS START AND END TOGETHER")
    print('{} and {}'
          .format(popular_start_end_stations['Start Station'].iloc[0], 
                  popular_start_end_stations['End Station'].iloc[0]
                  ))
    print('Number of occurrences: {}'.format(popular_start_end_stations['count'].iloc[0]))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()


    print("\nSUMMARY DETAILS (AVERAGE AND TOTAL TIME)")
    print('Total Travel Time: {} seconds and {} in hours'.format(total_travel_time, total_travel_time//60))
    print('Mean Travel Time: {} seconds and {} in hours'.format(mean_travel_time, mean_travel_time//60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts().rename_axis('User Type').reset_index(name='counts')
    print("\nUSER TYPE DETAILS")
    print("Subscribers: {} \nCustomers: {}".format(user_counts['counts'].iloc[1], user_counts['counts'].iloc[1]))


    # Display counts of gender
    print("\nGENDER DETAILS:")
    
    try: 
        gender_counts = df['Gender'].value_counts().rename_axis('Gender').reset_index(name='counts')
        print("Males: {} \nFemales: {}".format(gender_counts['counts'].iloc[0], gender_counts['counts'].iloc[1]))
        print(gender_counts)
    except:
        print('Gender column not available for this city')
    

    # Display earliest, most recent, and most common year of birth
    print("\nYEAR OF BIRTH DETAILS:")
    
    try:
        earliest_birth_year = df.sort_values(by=['Birth Year'])['Birth Year'].iloc[0]
        recent_birth_year = df.sort_values(by=['Birth Year'], ascending=False)['Birth Year'].iloc[0]
        popular_birth_year = df['Birth Year'].mode()[0]

        print("Earliest year of birth: {}".format(earliest_birth_year))
        print("Recent year of birth: {}".format(recent_birth_year))
        print('Popular Birth Year: {}'.format(popular_birth_year))
    except:
        print('Birth Year column not available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    while True:
        a = 0
        b = 5
        
        display_input = input("Do you want to view individual data? (Yes/No)\n")
        if display_input.lower() == "yes":
            print(df.iloc[a:b, :])
            a+=5
            b+=5
        else:
            break
                


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
