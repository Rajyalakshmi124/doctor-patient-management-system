import pymysql
 
class Database:
    def __init__(self):
        self.connection = None
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "trainingPoc"
        }
 
    #Establish a database connection.
    def connect(self):
        try:
            self.connection = pymysql.connect(**self.db_config)
            print("Database Connected Successfully")
            return self.connection
        except pymysql.MySQLError as e:
            print(f"Database Connection Error: {e}")
            return None
        
    #Return a cursor object to execute queries.
    def get_cursor(self):
        conn = self.connect()
        if conn:
            return conn.cursor()
        return None
    #Close the database connection.
    def close(self):
 
        if self.connection:
            self.connection.close()
            print("Database Connection Closed")
            self.connection = None
