import pandas as pd
import numpy as np
import time
# this is a bikeshare project welcome 😊
""" this project to explore US bikeshare data for three cities (chicago, New York, and Washington) """

CITY_DATA = {'chicago':'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington':'washington.csv'}

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def ret_filters():
    """asks user to inter a city, month, and day to analyze"""
    print("Hello! please inter some US bikeshare data")

    while True:
        city=input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
        if city in cities:
            break
        else:
            print("Please enter valid city name")

    while True:
        choice=input("Would you like to filter the data by month, day, or not at all?\n").lower()

        if choice =='month':
            month=input(" Which month - January, February, March, April, May, or June?\n")
            day='all'
            if month in months:
                break
            else:
                print("Please enter valid month name")
        elif choice == 'day':
            day=input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
            month='all'
            if day in days:
                break
            else:
                print("Please enter valid day name")

        elif choice == 'none':
            month='all'
            day = 'all'
            break
    print('-'*40)
    return city,month,day
 
def load_data(city, month, day):
   
    """Loads data for the specified city and filters by month and day if applicable."""
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all': 
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month

    # Mapping month numbers to names
    month_names = ["January", "February", "March", "April", "May", "June"]
    popular_month = month_names[df['month'].mode()[0] - 1]
    print('Most Common Month: \n', popular_month)

    popular_day = df['Start Time'].dt.day_name().mode()[0]
    print('Most Common Day of the Week: \n', popular_day) 

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    # Converting hour to 12-hour format with AM/PM
    am_pm = "AM" if popular_hour < 12 else "PM"
    popular_hour = popular_hour if popular_hour <= 12 else popular_hour - 12
    print('Most Common Start Hour: \n', popular_hour, am_pm)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: \n", popular_start_station)
    
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: \n", popular_end_station)
    
    combo_station = df['Start Station'] + " to " +  df['End Station']
    common_combo_station = combo_station.mode()[0]
    print("Most Common Trip from Start to End:\n {}".format(common_combo_station)) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def format_duration(duration):
        hour, remainder = divmod(duration, 3600)
        minute, second = divmod(remainder, 60)
        return hour, minute, second
    
    # Calculate total and average duration
    total_duration = df['Trip Duration'].sum()
    average_duration = df['Trip Duration'].mean()

    # Format and print total duration
    total_hour, total_minute, total_second = format_duration(total_duration)
    print("The Total Travel Time is {} Hours, {} Minutes, and {} Seconds.".format(total_hour, total_minute, total_second))

    # Format and print average duration
    avg_hour, avg_minute, avg_second = format_duration(round(average_duration))
    if avg_hour > 0:
        print('The Average Travel Time is {} Hours, {} Minutes, and {} Seconds.'.format(avg_hour, avg_minute, avg_second))
    else:
        print('The Average Trip Duration is {} Minutes and {} Seconds.'.format(avg_minute, avg_second))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    user_types = df['User Type'].value_counts()
    print("Counts of Each User Type:\n", user_types)

    
    try:
        gender = df['Gender'].value_counts()
        print(' ' * 40)
        print('Counts of Each User Gender:')
        print(gender)
    except:
        print('Counts of Each User Gender:\nSorry, no gender data available for {} City'.format(city.title()))
      
    
    try:
        earliest = df['Birth Year'].min() #Oldest birth year
        recent = df['Birth Year'].max() #Youngest birth Year
        common = df['Birth Year'].mode() #This gives the Common Birth Year 
        print(' ' * 40)
        print('Counts of User Birth Year:')
        print('Oldest User(s) Birth Year: ', int(earliest))
        print('Youngest User(s) Birth Year: ', int(recent))
        print('Most Common Birth Year: ', int(common))
    except:
        print('Counts of User Birth Year:\nSorry, no birth year data available for {} City'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)  

def individual_data(df):
   
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break


def main():
    while True:
        city, month, day = ret_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))
        
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()