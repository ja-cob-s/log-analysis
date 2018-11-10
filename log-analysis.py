#!/usr/bin/env python3

import psycopg2
DB_NAME = "news"

query1Title = "What are the most popular three articles of all time?"
query1 = ("select title, count(*) as views from articles "
          "join log on articles.slug = substring(log.path, 10) "
          "group by title order by views desc limit 3;")

query2Title = "Who are the most popular article authors of all time?"
query2 = ("select authors.name, count(*) as views from articles "
          "join authors on articles.author = authors.id "
          "join log on articles.slug = substring(log.path, 10) "
          "where log.status like '%200%' "
          "group by authors.name order by views desc;")

query3Title = "On which days did more than 1% of requests lead to errors?"
query3 = ("select day, perc from "
          "    (select day, round((sum(requests) / "
          "        (select count(*) from log "
          "        where substring(cast(log.time as text), 0, 11) = day) "
          "    * 100), 2) as perc from "
          "        (select substring(cast(log.time as text), 0, 11) "
          "        as day, count(*) as requests from log "
          "        where status like '%404%' group by day) "
          "    as log_perc group by day order by perc desc) "
          "as outer_query where perc >= 1;")


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
def printQueryResults(queryResult):
    for i in range(len(queryResult)):
        title = queryResult[i][0]
        views = queryResult[i][1]
        print("\t" + str(i + 1) + " - %s - %d" % (title, views) + " views")
    print("\n")


query1Results = getQueryResults(query1)
query2Results = getQueryResults(query2)
query3Results = getQueryResults(query3)

print(query1Title)
printQueryResults(query1Results)
print(query2Title)
printQueryResults(query2Results)
print(query3Title)
print("\t" + str(query3Results[0][0]) + " - " + str(query3Results[0][1]) + "%")
