from pickletools import read_uint1
import pandas as pd
import numpy as np
# import seaborn as sns
from os import listdir
from os.path import isfile, join
import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st
import datetime as dt
import ast
import json
import streamlit as st

# Function to preprocess the data
# @st.cache
def preprocess(df):
    df.drop_duplicates(subset=['Tweet Id'], keep="first", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Hashtags'].fillna('', inplace=True)
    df['Users Mentioned'].fillna('', inplace=True)
    df['Quoted Tweet'].fillna('', inplace=True)
    df['Reply to Tweet Id'].fillna(0, inplace=True)
    df['Reply to User'].fillna('', inplace=True)
    df['Retweeted Tweet'].fillna(0, inplace=True)
    df['Outlinks'].fillna('', inplace=True)
    df['place'].fillna('', inplace=True)
    df['Coordinates'].fillna('', inplace=True)
    # Tweet date
    df['Temp Date'] = df['Date'].astype(str)
    df['Date'] = df['Temp Date'].apply(lambda x: x.split(' ')[0])
    df['Time'] = df['Temp Date'].apply(lambda x: x.split('+')[0].split(' ')[1])
    df['Tweet Year'] = df['Date'].apply(lambda x: x.split('-')[0])
    df.drop('Temp Date', axis=1, inplace=True)
    # User Creation date
    df['Temp Date'] = df['User Created'].astype(str)
    df['User Created Date'] = df['Temp Date'].apply(lambda x: x.split(' ')[0])
    df['User Created Time'] = df['Temp Date'].apply(lambda x: x.split('+')[0].split(' ')[1])
    df['User Created Year'] = df['User Created Date'].apply(lambda x: x.split('-')[0])
    df.drop('Temp Date', axis=1, inplace=True)
    df.sort_values(by='Date', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

# Timeline Graph Function
# @st.cache
def timeline_graph(df):
    # creating a dateframe to capture date and tweets
    date_df = df['Date'].value_counts()
    date_df = pd.DataFrame(date_df)
    date_df.reset_index(inplace=True)
    date_df = date_df.rename(columns= {'index' : 'date', 'Date' : 'count'})
    date_df = date_df.sort_values(by='date', ascending=True)

    title = 'Tweets / Replies Timeline'
    labels = ['Posts', 'Tweets']
    colors = ['crimson', 'rgb(49,130,189)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    mode_size = [8, 8, 12, 8]
    line_size = [2, 2, 4, 2]

    try:
        x_data = np.array([date_df['date']
                        ])

        y_data = np.array([
            date_df['count']
        ])

        fig = go.Figure()

        for i in range(0, 1):
            fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                name=labels[i],
                line=dict(color=colors[i], width=line_size[i]),
                connectgaps=True,
            ))

            # endpoints
        #     fig.add_trace(go.Scatter(
        #         x=[x_data[i][0], x_data[i][-1]],
        #         y=[y_data[i][0], y_data[i][-1]],
        #         mode='markers',
        #         marker=dict(color=colors[i], size=mode_size[i])
        #     ))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=True,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=True,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.01, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text= ' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.85, y=y_trace[1],
                                        xanchor='left', yanchor='middle',
                                        text=' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.15,
                                    xanchor='left', yanchor='bottom',
                                    text='Posts Timeline',
                                    font=dict(family='Arial',
                                                size=30,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.0,
                                    xanchor='center', yanchor='top',
                                    text='Tweets done on the topic' +
                                        ' <br> ',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.5,
                                    xanchor='center', yanchor='top',
                                    text='Time Series with Range Slider ' +
                                        '',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)
        fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 day", step="day", stepmode="backward"),
                    dict(count=6, label="7 days", step="day", stepmode="backward"),
                    dict(count=1, label="1 month", step="month", stepmode="backward"),
                    dict(count=2, label="2 months", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ))

        # pyo.plot(fig, filename='nageswara_rao_post_timeline.html')
        # py.plot(fig, filename='nageswara_rao_post_timeline')

        st.markdown('Timeline of the keyword')
        st.plotly_chart(fig)
    except:
        pass

# Hashtag Graph Function
# @st.cache
def hashtag_graph(df):
    all_hashtags = list()
    try:
        for hashtags in df['Hashtags']:
            if len(hashtags) > 1:
                hashtags = ast.literal_eval(str(hashtags))
                for hashtag in hashtags:
                    all_hashtags.append(hashtag)
                    
        hashtag_df = pd.DataFrame({'Hashtags' : all_hashtags})
        hashtag_df = hashtag_df['Hashtags'].value_counts()
        hashtag_df = pd.DataFrame(hashtag_df)
        hashtag_df.reset_index(inplace=True)
        hashtag_df = hashtag_df.rename(columns= {'index' : 'hashtags', 'Hashtags' : 'count'})
    
    
        title = 'Common Re-Tweeters'
        labels = ['Accounts with The Hashtag', 'Newspaper', 'Internet', 'Radio']
        colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

        colors = ['black',] * 25
        colors[0] = 'crimson'
        colors[1] = '#004ecb'
        colors[2] = '#004ecb'
        colors[3] = 'lightslategray'
        colors[4] = 'lightslategray'
        colors[5] = 'lightslategray'
        colors[6] = 'lightslategray'

        mode_size = [8, 8, 12, 8]
        line_size = [2, 2, 4, 2]

        x_data = np.array([hashtag_df['hashtags'].head(20)])

        y_data = np.array([
            hashtag_df['count'].head(20)
        ])

        fig = go.Figure()

        # fig = go.Figure(data=[go.Bar(
        #     x=dghc_user_mention_freq_merged_df['username'].head(10),
        #     y=dghc_user_mention_freq_merged_df['occurrence'].head(10),
        #     marker_color=colors, # marker color can be a single color value or an iterable
        # )])

        for i in range(0, 1):
            fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i],
                name=labels[i],
                mode='markers',
                marker_color=colors
        #         text= y_data[i]
            ))

            # endpoints
            # fig.add_trace(go.Scatter(
            #     x=[x_data[i][0], x_data[i][-1]],
            #     y=[y_data[i][0], y_data[i][-1]],
            #     mode='markers',
            #     # marker=dict(color=colors[i], size=mode_size[i]),
            #     marker_color=colors,
            # ))

            # fig.add_shape(type="line",
            #     x0=1, y0=0, x1=x_data[i], y1=y_data[i],
            #     line=dict(color="RoyalBlue",width=3)
            # )

        for i in range(0, len(hashtag_df['hashtags'].head(20))):
            fig.add_shape(type='line',
                x0 = hashtag_df['hashtags'][i], y0 = i,
                x1 = hashtag_df['hashtags'][i],
                y1 = hashtag_df['count'][i],
                line=dict(color='rgb(115,115,115)', width = 1))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=False,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=False,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.03, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text='Count ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.5, y=2.2,
                                        xanchor='left', yanchor='middle',
                                        text='',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.10,
                                    xanchor='left', yanchor='bottom',
                                    text='Hashtags Used',
                                    font=dict(family='Arial',
                                                size=30,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.08,
                                    xanchor='center', yanchor='top',
                                    text='Hashtags that were mostly used on the topic ' +
                                        '<br> <br>',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)

        # pyo.plot(fig, filename='save_mathura_masjid_accounts_mentioned.html')
        # py.plot(fig, filename='save_mathura_masjid_accounts_mentioned')

        st.markdown('Hashtags Used')
        st.plotly_chart(fig)
    except:
        pass

# Account Tweeted Graph Function
# @st.cache
def accounts_tweeted_graph(df):
    # User who Tweeted on Hashtag
    username_df = df['Username'].value_counts()
    username_df = pd.DataFrame(username_df)
    username_df.reset_index(inplace=True)
    username_df = username_df.rename(columns= {'index' : 'Account', 'Username' : 'Occurrence'})
    
    try:
        title = 'Common Re-Tweeters'
        labels = ['Accounts with The Hashtag', 'Newspaper', 'Internet', 'Radio']
        colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

        colors = ['black',] * 25
        colors[0] = '#004ecb'
        colors[1] = '#004ecb'
        colors[2] = '#004ecb'
        colors[3] = 'lightslategray'
        colors[4] = 'lightslategray'
        colors[5] = 'lightslategray'
        colors[6] = 'lightslategray'

        mode_size = [8, 8, 12, 8]
        line_size = [2, 2, 4, 2]

        x_data = np.array([username_df['Account'].head(25)])

        y_data = np.array([
            username_df['Occurrence'].head(25)
        ])

        fig = go.Figure()

        # fig = go.Figure(data=[go.Bar(
        #     x=dghc_user_mention_freq_merged_df['username'].head(10),
        #     y=dghc_user_mention_freq_merged_df['occurrence'].head(10),
        #     marker_color=colors, # marker color can be a single color value or an iterable
        # )])

        for i in range(0, 1):
            fig.add_trace(go.Bar(x=x_data[i], y=y_data[i],
                name=labels[i],
                marker_color=colors,
        #         text= y_data[i]
            ))

            # endpoints
        #     fig.add_trace(go.Scatter(
        #         x=[x_data[i][0], x_data[i][-1]],
        #         y=[y_data[i][0], y_data[i][-1]],
        #         mode='markers',
        #         marker=dict(color=colors[i], size=mode_size[i])
        #     ))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=False,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=False,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.03, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text='Count ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.5, y=2.2,
                                        xanchor='left', yanchor='middle',
                                        text='',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.10,
                                    xanchor='left', yanchor='bottom',
                                    text='Accounts Tweeted',
                                    font=dict(family='Arial',
                                                size=30,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.08,
                                    xanchor='center', yanchor='top',
                                    text='Accounts who mostly tweeted on the topic ' +
                                        '<br><br>',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)

        # pyo.plot(fig, filename='save_mathura_masjid_accounts_mentioned.html')
        # py.plot(fig, filename='save_mathura_masjid_accounts_mentioned')

        st.markdown('Accounts Tweeted The Most')
        st.plotly_chart(fig)
    except:
        pass

# Verified Account Graph Function
# @st.cache
def verified_graph(df):
    verified_users = df[df['User Verified'] == True]
    verified_users.drop_duplicates(subset=['User Id'], keep="first", inplace=True)
    verified_users.reset_index(drop=True, inplace=True)
    
    try:
        # Calculating Size
        size_list = []
        for followers_count in verified_users['User Followers']:
            size = float(followers_count / 2500)
            if size > 150:
                size = 150
            elif size < 10:
                size = 10
            size_list.append(size)
        verified_users['Size'] = size_list

        # Top followers dataframe
        verified_followers = verified_users.sort_values(by=['User Followers'], ascending=False).head(35)
        
        title = 'Verified Accounts Involved'
        labels = ['Followers <br>Count']
        colors = ['rgb(49,130,189)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

        mode_size = [8, 8, 12, 8]
        line_size = [2, 2, 4, 2]

        x_data = np.array([verified_followers['Username']])

        y_data = np.array([
            verified_followers['User Followers']
        ])

        fig = go.Figure()

        for i in range(0, 1):
            fig.add_trace(go.Scatter(x=verified_followers['Username'], y = verified_followers['User Followers'], 
                            text=verified_followers['Username'], mode='markers', 
                            marker=dict(size=verified_followers['Size'], color=verified_followers['User Followers'],
                                        colorscale = "RdBu", colorbar_title = 'Followers <br>',
                            showscale=True)))

            # endpoints
        #     fig.add_trace(go.Scatter(
        #         x=[x_data[i][0], x_data[i][-1]],
        #         y=[y_data[i][0], y_data[i][-1]],
        #         mode='markers',
        #         marker=dict(color=colors[i], size=mode_size[i])
        #     ))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=True,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=False,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.01, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text=label + ' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.75, y=1.0,
                                        xanchor='left', yanchor='top',
                                        text=' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                    xanchor='left', yanchor='bottom',
                                    text='Verified Accounts Tweeted',
                                    font=dict(family='Arial',
                                                size=25,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.04,
                                    xanchor='center', yanchor='top',
                                    text='Verified twitter accounts who tweeted on the topic' +
                                        ' ',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)

        # pyo.plot(fig, filename='boycott_india_verified_accounts.html')
        # py.plot(fig, filename='boycott_india_verified_accounts.html')

        st.markdown('Verified Accounts Tweeted')
        st.plotly_chart(fig)
    except:
        pass

# Non Verified Account Graph Function
# @st.cache
def non_verified_graph(df):
    non_verified_users = df[df['User Verified'] == False]
    non_verified_users.drop_duplicates(subset=['User Id'], keep="first", inplace=True)
    non_verified_users.reset_index(drop=True, inplace=True)
    
    try:
        # Calculating Size
        size_list = []
        for followers_count in non_verified_users['User Followers']:
            size = float(followers_count / 2500)
            if size > 150:
                size = 150
            elif size < 10:
                size = 10
            size_list.append(size)
        non_verified_users['Size'] = size_list

        # Top followers dataframe
        non_verified_followers = non_verified_users.sort_values(by=['User Followers'], ascending=False).head(35)
        
        ####################################### Graph ############################################
        title = 'Verified Accounts Involved'
        labels = ['Followers <br>Count']
        colors = ['rgb(49,130,189)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

        mode_size = [8, 8, 12, 8]
        line_size = [2, 2, 4, 2]

        x_data = np.array([non_verified_followers['Username']])

        y_data = np.array([
            non_verified_followers['User Followers']
        ])

        fig = go.Figure()

        for i in range(0, 1):
            fig.add_trace(go.Scatter(x=non_verified_followers['Username'], y = non_verified_followers['User Followers'], 
                            text=non_verified_followers['Username'], mode='markers', 
                            marker=dict(size=non_verified_followers['Size'], color=non_verified_followers['User Followers'],
                                        colorscale = "RdBu", colorbar_title = 'Followers <br>',
                            showscale=True)))

            # endpoints
        #     fig.add_trace(go.Scatter(
        #         x=[x_data[i][0], x_data[i][-1]],
        #         y=[y_data[i][0], y_data[i][-1]],
        #         mode='markers',
        #         marker=dict(color=colors[i], size=mode_size[i])
        #     ))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=True,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=False,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.01, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text=label + ' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.75, y=1.0,
                                        xanchor='left', yanchor='top',
                                        text=' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                    xanchor='left', yanchor='bottom',
                                    text='Non Verified Accounts Tweeted',
                                    font=dict(family='Arial',
                                                size=25,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.04,
                                    xanchor='center', yanchor='top',
                                    text='Non Verified twitter accounts who tweeted on the topic' +
                                        ' ',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)

        # pyo.plot(fig, filename='boycott_india_verified_accounts.html')
        # py.plot(fig, filename='boycott_india_verified_accounts.html')

        st.markdown('Non-Verified Accounts Tweeted')
        st.plotly_chart(fig)
    except:
        pass

def users_ratio_graph(df):
    pass

# User Timeline Graph Function
# @st.cache
def user_timeline_graph(df):
    # User creation timeline
    unique_users_df = df.drop_duplicates(subset=['User Id'], keep="first")
    unique_users_df.reset_index(drop=True, inplace=True)
    user_date_df = unique_users_df['User Created Date'].value_counts()
    user_date_df = pd.DataFrame(user_date_df)
    user_date_df.reset_index(inplace=True)
    user_date_df = user_date_df.rename(columns= {'index' : 'date', 'User Created Date' : 'count'})
    user_date_df = user_date_df.sort_values(by='date')
    
    try:
        title = 'Tweets / Replies Timeline'
        labels = ['Accounts', 'Tweets']
        colors = ['crimson', 'rgb(49,130,189)', 'rgb(49,130,189)', 'rgb(189,189,189)']

        mode_size = [8, 8, 12, 8]
        line_size = [2, 2, 4, 2]

        x_data = np.array([user_date_df['date']
                        ])

        y_data = np.array([
            user_date_df['count']
        ])

        fig = go.Figure()

        for i in range(0, 1):
            fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                name=labels[i],
                line=dict(color=colors[i], width=line_size[i]),
                connectgaps=True,
            ))

            # endpoints
        #     fig.add_trace(go.Scatter(
        #         x=[x_data[i][0], x_data[i][-1]],
        #         y=[y_data[i][0], y_data[i][-1]],
        #         mode='markers',
        #         marker=dict(color=colors[i], size=mode_size[i])
        #     ))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=True,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=True,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.01, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text= ' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.85, y=y_trace[1],
                                        xanchor='left', yanchor='middle',
                                        text=' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.15,
                                    xanchor='left', yanchor='bottom',
                                    text='User Creation Timeline',
                                    font=dict(family='Arial',
                                                size=30,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.0,
                                    xanchor='center', yanchor='top',
                                    text='Creation timeline of accounts who tweeted on the topic' +
                                        ' <br> ',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.5,
                                    xanchor='center', yanchor='top',
                                    text='Time Series with Range Slider ' +
                                        '',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)
        fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 day", step="day", stepmode="backward"),
                    dict(count=6, label="7 days", step="day", stepmode="backward"),
                    dict(count=1, label="1 month", step="month", stepmode="backward"),
                    dict(count=2, label="2 months", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ))

        # pyo.plot(fig, filename='nageswara_rao_post_timeline.html')
        # py.plot(fig, filename='nageswara_rao_post_timeline')

        st.markdown('Accounts Creation Timeline')
        st.plotly_chart(fig)
    except:
        pass

def user_creation_annually(df):
    try:
        unique_users_df = df.drop_duplicates(subset=['User Id'], keep="first")
        unique_users_df.reset_index(drop=True, inplace=True)

        # user_location_df['location'].value_counts()
        unique_users_tweets_df = unique_users_df['Tweet Year'].value_counts()
        unique_users_tweets_df = pd.DataFrame(unique_users_tweets_df)
        unique_users_tweets_df.reset_index(inplace=True)
        unique_users_tweets_df = unique_users_tweets_df.rename(columns= {'index' : 'Year', 'Tweet Year' : 'Tweets'})


        label_colors = ['crimson', 'rgb(79, 129, 102)', 'rgb(129, 180, 179)', 'rgb(124, 103, 37)', 'rgb(146, 123, 21)', 'rgb(177, 180, 34)']

        fig = go.Figure(data=[go.Pie(labels=unique_users_tweets_df['Year'], values=unique_users_tweets_df['Tweets'], textinfo='label+percent',
                                    insidetextorientation='radial', marker_colors=label_colors
                                    )])
        fig.update_traces(hoverinfo='label+percent+name', hole=.25)
        fig.update(layout_title_text='Creation of accounts who all tweeted on the topic',
                layout_showlegend=True)
        st.markdown('Accounts Created Annually')
        st.plotly_chart(fig)
    except:
        pass

# Fetching Data
# path = "data/"
# file = "football"
# ext = ".csv"
# data_df = pd.read_csv(path + file + ext)

# Pre-processing dataframe
# preprocess(data_df)
# timeline_graph(data_df)