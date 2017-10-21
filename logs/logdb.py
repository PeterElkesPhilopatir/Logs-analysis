#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def get_most_popular3_articles():
    # Return the most 3 articles from the 'database'
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # First Method
    # c.execute("select title,views from articles "
    #           "order by (views) desc limit 3;")

    # Second method with no change in database
    c.execute(
        "select articles.title as title,count (*) as views "
        "from "
        "articles join log on log.path "
        "like "
        "concat('%',articles.slug,'%') "
        "group by "
        "title order by views desc"
        " limit 3;")

    data = c.fetchall()
    db.close()
    return data


def get_most_popular_article_authors():
    # Return the most 3 article authors from the 'database'
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # First method
    c.execute(
        "select authors.name as name, sum (views) from authors "
        "join articles on authors.id = articles.author "
        "group by (name) order by (sum) desc;")

    # Second Method with no change in database
    c.execute("select authors.name as name ,count (*) as views"
              " from articles "
              "join"
              " authors on articles.author = authors.id "
              "join "
              "log on log.path "
              "like concat ('%',articles.slug,'%')"
              " group by name "
              "order by views desc;")
    data = c.fetchall()
    db.close()
    return data


def get_date_errors():
    # Return the days did more than 1% of requests >>
    # lead to errors from the 'datebase'
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT E.date,(E.errors*1.0 / T.total_access)"
              " * 100 percentage " +
              "FROM" +
              "(select to_date(to_char(LOG.time,'YYYY/MM/DD'),'YYYY/MM/DD')"
              " as date,count(id)" +
              "errors FROM LOG where (status = '404 NOT FOUND')"
              " group by(date)) E " +
              "JOIN " +
              "(select to_date(to_char(LOG.time,'YYYY/MM/DD'),'YYYY/MM/DD')"
              " as date,count(id) " +
              "total_access FROM LOG group by(date)) T " +
              "ON E.date = T.date " +
              "WHERE (E.errors*1.0 / T.total_access) * 100 > 1;")
    data = c.fetchall()
    db.close()
    return data
