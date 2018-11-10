#!/usr/bin/env python3

import psycopg2
DB_NAME = "news"

query1Title = "What are the most popular three articles of all time?"
query1 = ("SELECT title, count(*) AS views FROM articles "
          "JOIN log ON substring(log.path, 10) = articles.slug "
          "GROUP BY title ORDER BY views DESC LIMIT 3;")

query2Title = "Who are the most popular article authors of all time?"
query2 = ("SELECT authors.name, count(*) AS views FROM articles "
          "JOIN authors ON authors.id = articles.author "
          "JOIN log ON substring(log.path, 10) = articles.slug "
          "WHERE log.status LIKE '%200%' "
          "GROUP BY authors.name ORDER BY views DESC;")

query3Title = "On which days did more than 1% of requests lead to errors?"
query3 = ("SELECT day, perc FROM "
          "    (SELECT day, round((sum(requests) / "
          "        (SELECT count(*) FROM log "
          "        WHERE log.time::date = day) "
          "    * 100), 2) AS perc FROM "
          "        (SELECT log.time::date "
          "        AS day, count(*) AS requests FROM log "
          "        WHERE status LIKE '%404%' GROUP BY day) "
          "    AS req_by_day GROUP BY day ORDER BY perc DESC) "
          "AS perc_by_day WHERE perc >= 1;")


# Connect to database
def connect():
    try:
        db = psycopg2.connect(database=DB_NAME)
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to the database")


# Return query result
def getQueryResults(query):
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


# For queries 1 and 2
def printQueryResults(result):
    for i in range(len(result)):
        title = result[i][0]
        views = result[i][1]
        print("\t" + str(i + 1) + " - " + title + " - " + str(views) + " views")


query1Results = getQueryResults(query1)
query2Results = getQueryResults(query2)
query3Results = getQueryResults(query3)

print(query1Title)
printQueryResults(query1Results)
print("\n")
print(query2Title)
printQueryResults(query2Results)
print("\n")
print(query3Title)
print("\t" + str(query3Results[0][0]) + " - " + str(query3Results[0][1]) + "%")
