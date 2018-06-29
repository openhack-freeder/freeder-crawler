import csv
import pymysql

conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='test',charset='utf8')
cur = conn.cursor()

with open('go.csv') as csvfile:
    sp = csv.DictReader(csvfile)
    for row in sp:
        sql = 'insert into contents(idx, category, title,`date`,`time`,`where`,url) values (idx, "%s","%s","%s","%s","%s","%s")'%(str(row['category']),str(row['title']),str(row['date']),str(row['time']),str(row['where']),str(row['url']))
        cur.execute(sql)

conn.commit()
cur.close()

print("done")
