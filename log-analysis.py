#!/usr/bin/env python3

import psycopg2
DB_NAME = "news"

query1Title = "What are the most popular three articles of all time?"
query1 = ("SELECT title, count(*) AS views FROM articles "
          "JOIN log ON articles.slug = substring(log.path, 10) "
          "GROUP BY title ORDER BY views DESC limit 3;")

query2Title = "Who are the most popular article authors of all time?"
query2 = ("SELECT authors.name, count(*) AS views FROM articles "
          "JOIN authors ON articles.author = authors.id "
          "JOIN log ON articles.slug = substring(log.path, 10) "
          "WHERE log.status like '%200%' "
          "GROUP BY authors.name ORDER BY views DESC;")

query3Title = "On which days did more than 1% of requests lead to errors?"
query3 = ("SELECT day, perc FROM "
          "    (SELECT day, round((sum(requests) / "
          "        (SELECT count(*) FROM log "
          "        WHERE substring(cast(log.time AS text), 0, 11) = day) "
          "    * 100), 2) AS perc FROM "
          "        (SELECT substring(cast(log.time AS text), 0, 11) "
          "        AS day, count(*) AS requests FROM log "
          "        WHERE status like '%404%' GROUP BY day) "
          "    AS log_perc GROUP BY day ORDER BY perc DESC) "
          "AS outer_query WHERE perc >= 1;")


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
