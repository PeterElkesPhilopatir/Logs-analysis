#!/usr/bin/env python3
from flask import Flask
import logdb

app = Flask(__name__)


def most3articles():
    for title, views in logdb.get_most_popular3_articles():
        print(title)
        print(views)


def most_article_authors():
    for name, sum in logdb.get_most_popular_article_authors():
        print(name)
        print(sum)


def errors_day():
    for date, percentage in logdb.get_date_errors():
        print(date)
        print(percentage)


if __name__ == '__main__':
    print("hello Udacity")
    print("The most popular three articles of all time are ")
    most3articles()
    print("--------------")
    print("The most popular article authors of all time are ")
    most_article_authors()
    print("--------------")
    print("The days did more than 1% of requests lead to errors are ")
    errors_day()
