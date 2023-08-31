import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor, helper

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)

    df = preprocessor.preprocesses(data)

    # fetching the unique users
    df['user'] = df["user"].astype(str)
    user_list = df['user'].unique()
    user_list1 = list(user_list)
    user_list1.remove('group notification')
    user_list1.sort()
    user_list1.insert(0, "Overall")

    user_selected = st.sidebar.selectbox("Show Analysis with respect to", user_list1)

    # Adding button
    if st.sidebar.button("Show Analysis"):

        number_of_messages, number_of_words, number_of_media_files, links = helper.fetch_data(user_selected, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(number_of_messages)

        with col2:
            st.header("Total Words")
            st.title(len(number_of_words))
            # Don't print number_of_words because it will display the words not the digits

        with col3:
            st.header("Shared Media")
            st.title(number_of_media_files)

        with col4:
            st.header("Links Shared")
            st.title(links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(user_selected, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(user_selected, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_mapping(user_selected, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_mapping(user_selected, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title("Weekly Activity Map")
        user_heat_map = helper.activity_heat_map(user_selected, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heat_map)
        st.pyplot(fig)

        # Finding the busiest user in the group

        if user_selected == "Overall":
            st.title("Most busy user")
            x, new_df = helper.Busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud

        st.title("WordCloud")
        df_wc = helper.create_word_cloud(user_selected, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words

        st.title("Most Common Words")
        return_df = helper.most_common_words(user_selected, df)

        fig, ax = plt.subplots()
        ax.barh(return_df[0], return_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #st.dataframe(return_df)

        # Emoji Analysis

        emoji_df = helper.emoji_helper(user_selected, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels = emoji_df[0], autopct="%0.2f")
            st.pyplot(fig)
        #st.dataframe(emoji_df)