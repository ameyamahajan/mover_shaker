import pymysql
from config import ConfigApp
import datetime, sys

class TrackingFileDB():
    def __init__(self,conf):
        self.conf = conf

    def __get_connection(self):
        return pymysql.connect(host = '127.0.0.1',
                               user = 'zautomate',
                               password = 'zautomate',
                               #db = self.conf.conf_data.get('client_name'),
                               db='cloudharmonics',
                               cursorclass = pymysql.cursors.DictCursor
                               )

    def __execute_sql(self,SQL):
        result_set = None
        try:
            conn = self.__get_connection()
            cursor = conn.cursor()
            cursor.execute(SQL)
            print("Row returned "+str(cursor.rowcount))
            result_set = [cursor.fetchone()] if cursor.rowcount == 1 else cursor.fetchall()
            conn.commit()
        except Exception as ex:
            print(str(ex) + " : error occurred, while running the SQL"+ SQL)
        finally:
            conn.close()

        return result_set

    def add_file(self, file_name):
        """
        This function creates an entry for the file uploaded to the data portal.

        """
        #try:

        sql = """INSERT INTO file_tracker (process_date,update_date,filename, file_type, status)
            VALUES ('%s','%s','%s','%s','%s')"""%(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                                  datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                                  file_name,
                                                  file_name.split(".")[-1],
                                                  'uploaded')

        self.__execute_sql(sql)


    def get_status(self, file_name):
        """
        Check the status of the file based on the table value.
        """
        sql = """SELECT * FROM file_tracker WHERE filename = '%s'"""%(file_name)
        print("SQL :"+ sql)
        result_set = self.__execute_sql(sql)
        return result_set


    def get_recent(self):
        """
        Give the status of files upload in last month
        :return:
        """
        sql = """SELECT * FROM file_tracker
                WHERE process_date <= '%s'
                and process_date > '%s'
                """%(datetime.datetime.utcnow().strftime('%Y-%m-%d 23:59:59'),
                     (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'))

        print("SQL :" + sql)
        result_set = self.__execute_sql(sql)
        return result_set



if __name__=="__main__":
    con = ConfigApp('cloudharmonics')
    sc = TrackingFileDB(con)
    sc.add_file('test4.pos')
    sc.get_recent()
    sc.get_status('test.pos')
