from typing import NoReturn
from data_extraction import *
from html_script import make_html_report


def lambda_handler(event: dict, context: dict) -> NoReturn:
    rides = extract_last_day_data(LAST_DAY)
    num_of_rides = rides.shape[0]
    users = extract_last_day_users(rides)
    ages = extract_ages(users)
    genders = gender_distribution(users)
    gender_plot(genders)
    age_plot(ages)
    averages = extract_averages(rides)
    totals = extract_total(rides)
    make_html_report(num_of_rides, ages, genders, averages, totals)


lambda_handler({}, {})
