from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor = URLExtract()

def fetch_data(user_selected, df):

    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    # Fetching the number of messages
    number_of_messages = df['message'].shape[0]

    # fetching the total number of words
    number_of_words = []
    for i in df['message']:
        number_of_words.extend(i.split())

    # Fetching the number of media messages
    number_of_media_files = df[df['message'] =='<Media omitted>\n'].shape[0]

    # Fetching number of links shared
    links = []
    for k in df['message']:
        links.extend(extractor.find_urls(k))

    return number_of_messages, number_of_words, number_of_media_files, len(links)


def Busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df

def create_word_cloud(user_selected, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(user_selected, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_helper(user_selected, df):
    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(user_selected, df):
    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    timeline = df.groupby(['year', 'month_number', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(user_selected, df):
    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_mapping(user_selected, df):
    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    return df['day_name'].value_counts()

def month_activity_mapping(user_selected, df):
    if user_selected != "Overall":
        df = df[df['user'] == user_selected]
    return df['month'].value_counts()

def activity_heat_map(user_selected, df):
    if user_selected != "Overall":
        df = df[df['user'] == user_selected]

    user_heat_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heat_map