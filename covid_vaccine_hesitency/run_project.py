"""
Emily Giverts
CSE 163 AC

A file that runs the entire project.
"""

import general
import analyze_api
import pandas as pd


def main():
    """
    Runs all the project methods.
    """
    data = pd.read_csv(
           'covid_vaccine_hesitency/main_data/us-daily-covid-vaccine-doses-administered.csv')
    data = general.clean_data(data)
    general.bar(data)
    general.line(data)
    general.geo(data)
    general.income(data)
    general.max_min_inc(data)
    general.min_max_vacc_rate(data)

    api_data = pd.read_csv('covid_vaccine_hesitency/main_data/newapidata.csv')
    api_data['Tweet'] = api_data['Tweet'].apply(analyze_api.clean_data)
    api_data['Subjectivity'] = api_data['Tweet'].apply(
                               analyze_api.getSubjectivity)
    api_data['Polarity'] = api_data['Tweet'].apply(analyze_api.getPolarity)
    analyze_api.make_cloud(api_data)
    api_data['Analysis'] = api_data['Polarity'].apply(analyze_api.get_analysis)
    analyze_api.location_analysis(api_data)
    analyze_api.geo(api_data)


if __name__ == '__main__':
    main()