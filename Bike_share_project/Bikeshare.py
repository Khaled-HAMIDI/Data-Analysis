import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by (0,1,2, ... ,6) , or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
     # get user input for city
    while (True):
        city=input('Enter the city you want to have statistics for (Chicago ,New york city or Washington) \n  City:' )
        if city.lower() in ['chicago' , 'new york city' , 'washington']:
            break

    # get user input for month (all, january, february, ... , june)
    while (True):
        print('\nYou chose the city of {}'.format(city) )
        month=input('Now enter the month you want to filter by(january, february, ... , june),all if you want no filter \n  Month:')
        if (month.lower() in months) or (month == 'all'):
            break 

    # get user input for day of week (all,0,1, ... ,6)
    while (True):
        day=input('\nNow enter the day you want to filter by (0,1,2, ... ,6) ,all if you dont want to filter per day\n  Day: ')
        
        if day.lower() =='all':
            break
        elif (int(day) in range(0,7)) :
            break

    print('-'*40)
    return city,month,day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day -  of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month ,day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x:x.month)
    df['day'] = df['Start Time'].apply(lambda x:x.dayofweek)
    df['hour']=df['Start Time'].apply(lambda x:x.hour)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_nb=months.index(month.lower(  )) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_nb]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] ==int(day)]

    return df



def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if (month =='all'):
        month_max=df['month'].value_counts().head(1)
        print('the most common month is {} with count of  {} '.format( month_max.keys()[0] ,month_max.iloc[0]))


    # display the most common day of week
    if (day == 'all'):
        day_max=df['day'].value_counts().head(1)
        print('the most common day is day {} with count of  {} '.format( day_max.keys()[0] ,day_max.iloc[0]))

    # display the most common start hour
    hour_max=df['hour'].value_counts().head(1)
    print("the most common start hour is {}  with the count of  {} ".format( hour_max.keys()[0] ,hour_max.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_max=df['Start Station'].value_counts().head(1)
    print('The most common start station is  {}  with count of  {} '.format( start_max.keys()[0] ,start_max.iloc[0] ))
    
    # display most commonly used end station
    end_max=df['End Station'].value_counts().head(1)
    print('The most common end station is {}  with count of  {} \n'.format( end_max.keys()[0] ,end_max.iloc[0] ))


    # display most frequent combination of start station and end station trip
    freq_combination=df.groupby(['Start Station','End Station']).count()['Trip Duration'][df.groupby(['Start Station','End Station']).count()['Trip Duration']==df.groupby(['Start Station','End Station']).count()['Trip Duration'].max()]
    print('The most common combination of start and end station is  ')
    print('     The start station : {}'.format(freq_combination.keys()[0][0]) )
    print('     The end station  : {}'.format(freq_combination.keys()[0][1]) )
    print('     With the count of : {}'.format(freq_combination.iloc[0])) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is : {} '.format(df['Trip Duration'].sum())) 

    # display mean travel time
    print('The mean travel time  is : {} '.format( df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    #Verify if the datatframe conatins a collumn named 'Gender' and 'Birth Year' exp:washington
    if ('Gender' and 'Birth Year') in df :
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of gender
        print('Gender:')
       
        gender_1=df.groupby('Gender').count()['Trip Duration'].keys()[0]
        count_gender_1=df.groupby('Gender').count()['Trip Duration'].iloc[0]
        gender_2=df.groupby('Gender').count()['Trip Duration'].keys()[1]
        count_gender_2=df.groupby('Gender').count()['Trip Duration'].iloc[1]
       
        print ('We have  {}  of  {}  and  {}  of  {}'.format( count_gender_1,gender_1,count_gender_2,gender_2))
        
        # Display counts of user types
        print('\nUser types')

        user_type_1=df.groupby('User Type').count()['Trip Duration'].keys()[0]
        count_type_1=df.groupby('User Type').count()['Trip Duration'].iloc[0]
        user_type_2=df.groupby('User Type').count()['Trip Duration'].keys()[1]
        count_type_2=df.groupby('User Type').count()['Trip Duration'].iloc[1]

        print ('We have {}  of  {} and   {}  of  {}'.format(count_type_1 ,user_type_1 ,count_type_2,user_type_2))


        # Display earliest, most recent, and most common year of birth
        print('\nThe earliest year of birth is {} '.format(df['Birth Year'].min()))
        print('The most recent year of birth is {} '.format( df['Birth Year'].max()))
        print('The most common year of birth is {} '.format( df['Birth Year'].mode().iloc[0]))


        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print('\nThere are only user types stats for this city')
        start_time = time.time()
       
        print('\nUser types')
        print ('We have {}  of  {} and   {}  of  {} '.format(  df.groupby('User Type').count()['Trip Duration'].iloc[0]  ,df.groupby('User Type').count()['Trip Duration'].keys()[0] ,df.groupby('User Type').count()['Trip Duration'].iloc[1],df.groupby('User Type').count()['Trip Duration'].keys()[1]))
        print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def indiv_trip_data(df):
    '''Display the individual trip data'''
   
    i=0
    while (True):
        display=input('\nWould you like to view individual trip data ? (type yes or no)  ')
        if display.lower() != 'yes':
            break
        else:
            for j in range(5):
                print('-'*40)
                print('\n This is the raw number {} : '.format(i+1))

                #raw will conatain the pandas serie in json format 
                raw=df.iloc[i].to_json()
                raw_list=raw.split(',')

                #Display the raw in the specified format
                for item in raw_list:
                    print('\n {}'.format(item))
                i=i+1


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df,day,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        indiv_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
   
    main()
