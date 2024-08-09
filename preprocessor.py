import re
import pandas as pd

def preprocesses(data1):
    # Pattern to match date and time format in the chat
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # Split the data into messages and dates
    messages = re.split(pattern, data1)[1:]  # Skip the first element which will be empty
    dates = re.findall(pattern, data1)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Correct the date format string
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    
    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        write = re.split(r'([\w\W]+?):\s', message)
        if len(write) > 1:
            users.append(write[1])
            messages.append(write[2])
        else:
            users.append('group notification')
            messages.append(write[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add additional columns for date and time
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_number'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Add a period column
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-1")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
