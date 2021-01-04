import json
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime, date


def read_input_data():
    with open('data.json', 'r') as f:
        return json.load(f)


def get_salary_days(start_date, dates):
    return list(map(lambda x: (x - start_date).days, dates))


def get_trend_line_data(start_date, end_date, salary_days, salaries):
    polyfit = np.polyfit(salary_days, salaries, 1)
    trend_func = np.poly1d(polyfit)

    trend_dates = [start_date, end_date]
    trend_salary_days = get_salary_days(start_date, trend_dates)
    trend_salaries = list(map(lambda x: trend_func(x), trend_salary_days))

    return trend_dates, trend_salaries


def create_plot(x, y, trend_x, trend_y, title, xlabel, ylabel, line):
    plt.plot(x, y)
    plt.plot(trend_x, trend_y, line)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


if __name__ == '__main__':
    input_data = read_input_data()
    salary_data = input_data['salaries']
    last_trend_date = datetime.strptime(input_data['last_trend_date'], '%d.%m.%Y').date()

    dates = list(map(lambda x: datetime.strptime(x['date'], '%d.%m.%Y').date(), salary_data))
    ru_salaries = list(map(lambda x: x['ru_salary'], salary_data))
    usd_salaries = list(map(lambda x: x['ru_salary'] / x['usd_course'], salary_data))

    start_date = dates[0]
    salary_days = get_salary_days(start_date, dates)

    ru_trend_dates, ru_trend_salaries = get_trend_line_data(start_date, last_trend_date, salary_days, ru_salaries)
    usd_trend_dates, usd_trend_salaries = get_trend_line_data(start_date, last_trend_date, salary_days, usd_salaries)

    create_plot(dates, ru_salaries, ru_trend_dates, ru_trend_salaries, 'Salary in RUB', 'Date', 'Salary', '--')
    create_plot(dates, usd_salaries, usd_trend_dates, usd_trend_salaries, 'Salary in RUB', 'Date', 'Salary', '--')
