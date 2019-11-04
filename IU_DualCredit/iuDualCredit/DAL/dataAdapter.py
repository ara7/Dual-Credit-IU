from django.db import connection

def execute(sqlQuery):

    try:

        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        sqlList = cursor.fetchall()
        return sqlList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


def executeOne(sqlQuery):

    try:
        
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        sqlList = cursor.fetchone()
        return sqlList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


def ConvertToList(data, index):

    try:
        queryList = []
        for row in data:
            rowList = list(row)
            queryList.append(rowList[index])
        return queryList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


    
