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