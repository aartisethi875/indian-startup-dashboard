import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv('startup_data')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


colors = ["#E78CAE", "#926580", "#926580", "#707EA0", "#34495E"]
custom_palette = sns.color_palette(colors)


def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startup
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'cr')
    with col2:
        st.metric('Max', str(max_funding) + 'cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' cr')
    with col4:
        st.metric('Funded Startups', num_startups)

    col1, col2 = st.columns(2)
    with col1:
        st.header('MoM graph')
        selected_option = st.selectbox('Select Type', ['Total', 'count'])
        if selected_option == 'total':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

        temp_df['x_axis'] = temp_df['month'].astype('str') + '_' + temp_df['year'].astype('str')

        # Create plot
        fig5, ax = plt.subplots()
        ax.plot(temp_df['x_axis'], temp_df['amount'])

        # Set plot labels and title
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Total Amount' if selected_option == 'Total' else 'Transaction Count')
        ax.set_title('Month-on-Month Analysis')

        # Display plot in Streamlit
        st.pyplot(fig5)

    with col2:
        st.header('Top sectors')
        sector_option = st.selectbox('select Type ', ['total', 'count'])
        if sector_option == 'total':
            tmp_df = df.groupby(['vertical'])['amount'].sum().sort_values(ascending=False).head(5)
        else:
            tmp_df = df.groupby(['vertical'])['amount'].count().sort_values(ascending=False).head(5)

        fig7, ax7 = plt.subplots()
        ax7.pie(tmp_df, labels=tmp_df.index, autopct="%0.01f%%")
        st.pyplot(fig7)

    col1, col2, = st.columns(2)
    with col1:
        st.header('Type of funding')
        funding_series = df.groupby('round')['round'].count().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(funding_series.index, funding_series.values)
        st.pyplot(fig)

    with col2:
        st.header(' City wise funding')
        cityfun_series = df.groupby(['city'])['round'].count().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.bar(cityfun_series.index, cityfun_series.values)
        plt.title("City wise funding", fontsize=14)
        plt.xlabel("City", fontsize=14)
        plt.ylabel("Number of funding", fontsize=14)
        st.pyplot(fig)

    col1, col2, = st.columns(2)

    with col1:
        st.header('Top startups')
        top_startup = df.groupby(['startup'])['year'].count().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        ax.pie(top_startup, labels=top_startup.index, autopct='%0.001f%%', shadow=True, startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    with col2:
        st.header('top startup overall')
        overall_series = df.groupby(['startup'])['startup'].count().sort_values(ascending=False).head(8)
        fig, ax = plt.subplots()
        ax.bar(overall_series.index, overall_series.values)
        st.pyplot(fig)

    st.header('Funding Heatmap')
    table = pd.crosstab(df['year'], df['round'], values=df['amount'], aggfunc='sum')
    fig, ax = plt.subplots(figsize=(20,5))
    sns.heatmap(table,  cmap=custom_palette, vmin=0, vmax=1, annot_kws={"size": 14},
                ax=ax)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Funding Amount", fontsize=14)
    st.pyplot(fig)


def load_investor_details(investor):
    st.title(investor)
    # load the recent five investment of the investor
    lasts_5df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(lasts_5df)

    # biggest investment
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round Invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('city Invested in')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    col5, col6 = st.columns(2)
    with col5:
        df['Year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('Year')['amount'].sum()
        st.subheader('YOY Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)
        st.pyplot(fig4)

    with col6:
        similar_investors = df[df['investors'].str.contains(investor)].groupby('subvertical')['amount'].sum()
        st.subheader('similar investor')
        fig6, ax6 = plt.subplots()
        ax6.pie(similar_investors, labels=similar_investors.index, autopct="%0.01f%%")
        st.pyplot(fig6)


def load_startup_details(startup):
    st.title(startup)
    col1, col2 = st.columns(2)
    with col1:
        # investment details
        industry_series = df[df['startup'].str.contains(startup)][['year', 'vertical', 'city', 'round']]
        st.subheader('About startup')
        st.dataframe(industry_series)

    with col2:
        inv_series = df[df['startup'].str.contains(startup)].groupby('investors').sum()
        st.subheader('investors')
        st.dataframe(inv_series)

    # Subindustry
    col1, col2, col3 = st.columns(3)
    with col1:
        sub_series = df[df['startup'].str.contains(startup)].groupby('subvertical')['year'].sum()
        st.subheader('subindustry')
        fig9, ax9 = plt.subplots()
        ax9.pie(sub_series, labels=sub_series.index, autopct="%0.01f%%")
        st.pyplot(fig9)

    with col2:
        ver_series = df[df['startup'].str.contains(startup)].groupby('vertical')['year'].sum()
        st.subheader('industry')
        fig10, ax10 = plt.subplots()
        ax10.pie(ver_series, labels=ver_series.index, autopct="%0.01f%%")
        st.pyplot(fig10)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()


elif option == 'Startup':
    select_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(select_startup)

else:
    selected_investor = st.sidebar.selectbox('Select StartUp', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
