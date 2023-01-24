"""
Emily Giverts
CSE 163 AC

A file that tests the function implementations within run_project.py.
"""

import general
import analyze_api
import pandas as pd


def test_daily_vacc_per_state(vacc_data):
    general.line(vacc_data)


def test_geo_polarity(api_data):
    analyze_api.geo(api_data)


def test_geo_total_vacc(vacc_data):
    general.geo(vacc_data)


def test_location_analysis(api_data):
    analyze_api.location_analysis(api_data)


def test_min_max_bar(vacc_data):
    general.max_min_inc(vacc_data)


def test_min_max_daily_vacc(vacc_data):
    # should be empty graph, since mississippi and maryland aren't in vacc dataset
    general.min_max_vacc_rate(vacc_data)


def test_state_inc_comparison(vacc_data):
    general.income(vacc_data)


def test_total_vacc_per_state(vacc_data):
    general.bar(vacc_data)


def test_word_cloud(api_data):
    analyze_api.make_cloud(api_data)


def main():
    vacc_data = 'covid_vaccine_hesitency/test_data/Vacc_Test_Data.csv'
    vacc_data = pd.read_csv(vacc_data)
    test_daily_vacc_per_state(vacc_data)
    test_geo_total_vacc(vacc_data)
    test_min_max_bar(vacc_data)
    test_min_max_daily_vacc(vacc_data)
    test_state_inc_comparison(vacc_data)
    test_total_vacc_per_state(vacc_data)

    api_data = pd.read_csv('covid_vaccine_hesitency/test_data/API_Test_Data.csv')
    api_data['Tweet'] = api_data['Tweet'].apply(analyze_api.clean_data)
    api_data['Subjectivity'] = api_data['Tweet'].apply(
                               analyze_api.getSubjectivity)
    api_data['Polarity'] = api_data['Tweet'].apply(analyze_api.getPolarity)
    test_word_cloud(api_data)
    api_data['Analysis'] = api_data['Polarity'].apply(analyze_api.get_analysis)
    test_location_analysis(api_data)
    test_geo_polarity(api_data)


if __name__ == '__main__':
    main()