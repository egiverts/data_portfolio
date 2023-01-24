"""
Emily Giverts
CSE 163 AC

A file that processes state vaccination data as well as state yearly income
data. It also contains methods that analyzes various helper data sets and
creates visualizations exemplifying insights.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd


def clean_data(data):
    """
    Cleans the daily vaccination data set, filtering out extra
    territories not needed in this analysis. Returns the filtered out data.
    """
    data = data.loc[data['Entity'] != 'American Samoa', :]
    data = data.loc[data['Entity'] != 'Bureau of Prisons', :]
    data = data.loc[data['Entity'] != 'Dept of Defense', :]
    data = data.loc[data['Entity'] != 'District of Columbia', :]
    data = data.loc[data['Entity'] != 'Federated States of Micronesia', :]
    data = data.loc[data['Entity'] != 'Guam', :]
    data = data.loc[data['Entity'] != 'Indian Health Svc', :]
    data = data.loc[data['Entity'] != 'Long Term Care', :]
    data = data.loc[data['Entity'] != 'Marshall Islands', :]
    data = data.loc[data['Entity'] != 'Puerto Rico', :]
    data = data.loc[data['Entity'] != 'United States', :]
    data = data.loc[data['Entity'] != 'Veterans Health', :]
    data = data.loc[data['Entity'] != 'Virgin Islands', :]
    return data


def bar(data):
    """
    Plots a bar graph of the total vaccines in each state.
    """
    sns.catplot(kind="bar", data=data, x="Entity", y="daily_vaccinations")
    plt.title("Total Vaccinations in Each State")
    plt.xlabel('State')
    plt.ylabel('Total Vaccinations')
    plt.xticks(rotation=-60, fontsize=3)
    plt.savefig('total_vacc_per_state.png', bbox_inches='tight')


def line(data):
    """
    Plots a line egraph of the daily vaccinations over time in each state.
    """
    fig, ax = plt.subplots(1)
    sns.lineplot(data=data, x="Day", y="daily_vaccinations", hue="Entity",
                 style="Entity")
    ax.get_legend().remove()
    plt.title("Vaccinations Over Time in Each State")
    plt.xlabel('Day')
    plt.ylabel('Vaccines')
    plt.savefig('daily_vacc_per_state.png', bbox_inches='tight')


def geo(data):
    """
    Plots a map of the current total vaccinations within each state.
    """
    # Joins geo data with vaccine data
    country = gpd.read_file('covid_vaccine_hesitency/main_data/gz_2010_us_040_00_5m.json')
    country = country[country['NAME'] != 'Hawaii']
    country = country[country['NAME'] != 'Alaska']
    country = country[country['NAME'] != 'Puerto Rico']
    country_copy = country
    combined_data = data.merge(country, left_on='Entity', right_on='NAME')

    # Creates USA map and plots data
    fig, ax = plt.subplots(1)
    combined_data = gpd.GeoDataFrame(combined_data, geometry='geometry')
    # Filters out Alaska & Hawaii in order to visually look nicer
    combined_data = combined_data[(combined_data['Entity'] != 'Alaska') &
                                  (combined_data['Entity'] != 'Hawaii')]
    country_copy.plot(ax=ax, color='#EEEEEE')
    combined_data.plot(ax=ax, column='daily_vaccinations', legend=True)
    plt.title("Total Vaccinations in Each State")
    plt.savefig('geo_total_vacc.png')


def income(data):
    """
    Works with state based estimated yearly income dataset and plots two bar
    graphs side by side showing th comparison between states that
    average over $70,000 and their total vaccinations.
    """
    # Joins income data with vaccine data
    income_data = pd.read_csv('covid_vaccine_hesitency/main_data/GCT1901.csv')
    data = data.groupby('Entity')['daily_vaccinations'].sum()
    data = data.to_frame()
    combined_data = data.merge(income_data, left_on='Entity',
                               right_on='GEONAME')
    combined_data['ESTIMATE'] = combined_data['ESTIMATE'].replace(
                                                        ',', '', regex=True)
    # Filters out yearly income greater than $70,000
    check = combined_data['ESTIMATE'].astype(int) > 70000
    combined_data = combined_data[check]

    # Creating Visualization
    fig, axes = plt.subplots(1, 2, sharex=True, figsize=(16, 8))
    # Income graph
    combined_data['ESTIMATE'] = combined_data['ESTIMATE'].astype('float')
    sns.barplot(data=combined_data, x="GEONAME", y="ESTIMATE", ax=axes[0])
    axes[0].set(ylim=(60000, 90000))
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)
    axes[0].set(xlabel="State", ylabel="Estimated Annual Income")
    axes[0].set_title("Income of States Averaging Over $70K Annually")
    # Vaccination graph
    sns.barplot(data=combined_data, x="GEONAME", y="daily_vaccinations",
                ax=axes[1])
    axes[1].set_title("Vaccinations of States Averaging Over $70K Annually")
    axes[1].set(xlabel="State", ylabel="Total Vaccinations")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)
    fig.savefig('state_inc_comparison.png', bbox_inches='tight')


def max_min_inc(data):
    """
    Works with state based estimated yearly income dataset and plots two bar
    graphs side by side showing th comparison between states that
    average over $70,000 and their total vaccinations.
    """
    # Joining & filtering data
    income_data = pd.read_csv('covid_vaccine_hesitency/main_data/GCT1901.csv')
    data = data.groupby('Entity')['daily_vaccinations'].sum()
    data = data.to_frame()
    combined_data = data.merge(income_data, left_on='Entity',
                               right_on='GEONAME')
    combined_data['ESTIMATE'] = combined_data['ESTIMATE'].replace(
                                                        ',', '', regex=True)
    max_inc = combined_data['ESTIMATE'].max()
    min_inc = combined_data['ESTIMATE'].min()
    combined_data = combined_data[(combined_data['ESTIMATE'] == max_inc) |
                                  (combined_data['ESTIMATE'] == min_inc)]

    # creating visualzation
    fig, axes = plt.subplots(1, 2, sharex=True, figsize=(16, 8))
    # Income graph
    combined_data['ESTIMATE'] = combined_data['ESTIMATE'].astype('float')
    sns.barplot(data=combined_data, x="GEONAME", y="ESTIMATE", ax=axes[0])
    axes[0].set(ylim=(0, 90000))
    axes[0].set(xlabel="State", ylabel="Estimated Annual Income")
    axes[0].set_title("Income of States Averaging Over $70K Annually")
    # Vaccination graph
    sns.barplot(data=combined_data, x="GEONAME", y="daily_vaccinations",
                ax=axes[1])
    axes[1].set_title("Vaccinations of States Averaging Over $70K Annually")
    axes[1].set(xlabel="State", ylabel="Total Vaccinations")
    fig.savefig('min_max_bar.png', bbox_inches='tight')


def min_max_vacc_rate(data):
    """
    Works with state based estimated yearly income dataset and plots two bar
    graphs side by side showing th comparison between the states that makes
    estimated least amount of annual income vs the estimated most annual
    income and shows the comparison of the total vaccinations of those states.
    """
    # Filtering data (using Maryland & Mississippi)
    data = data[(data['Entity'] == 'Maryland') |
                (data['Entity'] == 'Mississippi')]
    # Plotting line graph
    sns.relplot(kind="line", data=data, x="Day", y="daily_vaccinations",
                hue="Entity", style="Entity")
    plt.title("Relationsip Between Min/Max Income and Vaccination Rate")
    plt.xlabel('Day')
    plt.ylabel('Vaccinated Individuals')
    plt.savefig('min_max_daily_vacc.png', bbox_inches='tight')