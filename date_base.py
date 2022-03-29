import mysql.connector
import datetime


class DataBase:
    def connection(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            database='minsk_events',
            # password = 'newpassword'
        )
        self.cursor = self.db.cursor()

    def insert_events(self, date, names, places, time, hrefs, href_text, category):
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {date}__{category} (id INT PRIMARY KEY AUTO_INCREMENT, name varchar(255),'
            f' place varchar(1255),'
            f' time varchar(127),'
            f' href varchar(1255),'
            f' href_text varchar(1255))')

        self.cursor.execute(f'DELETE FROM {date}__{category} ')
        self.db.commit()

        for i in range(len(names)):
            cursor_query = f'''INSERT INTO {date}__{category} (name, place, time, href, href_text) VALUES 
                ('{names[i]}',
                 '{places[i]}', 
                 '{time[i]}', 
                 '{hrefs[i]}', 
                 '{href_text[i]}')'''


            self.cursor.execute(cursor_query)
            self.db.commit()

        day = datetime.datetime.today() - datetime.timedelta(days=1)
        delete = day.strftime("%d_%m_%Y")

        self.cursor.execute(f'DROP TABLE IF EXISTS {delete}__{category}')
        self.db.commit()

    def read_db(self, number_of_month, category):
        try:
            select_all_events = f'SELECT * from {number_of_month}__{category}'
            self.cursor.execute(select_all_events)
            rows = self.cursor.fetchall()
            list_events = []
            for item in rows:
                list_events.append(item)
            self.db.close()
            return list_events
        except Exception as error:
            print(error)
            self.db.close()
            return 'empty'

    def insert_person(self, person):
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS persons (id INT PRIMARY KEY AUTO_INCREMENT, first_name varchar(255),'
            f' username varchar(255),'
            f' sex varchar(20),'
            f' age SMALLINT, time DATETIME)')

        find_time = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(f'SELECT * FROM persons WHERE time > "{find_time}"')
        persons = self.cursor.fetchall()
        for item in persons:
            if person['username'] == item[2]:
                return 'existed'

        insert_person = f'''INSERT INTO persons(first_name, username, sex, age, time) VALUES
         ('{person['first_name']}',
          '{person['username']}',
          '{person['sex']}',
          '{person['age']}',
          "{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")'''
        self.cursor.execute(insert_person)
        self.db.commit()
        self.db.close()
        return 'add'

    def show_people(self):
        self.cursor = self.db.cursor()
        find_time = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(f'SELECT * FROM persons WHERE time > "{find_time}"')
        persons = self.cursor.fetchall()
        return persons

    def show_all(self):
        self.cursor = self.db.cursor()
        self.cursor.execute(f'SELECT * FROM persons')
        persons = self.cursor.fetchall()
        self.db.close()
        return persons

    def delete_person(self, name):
        self.cursor.execute(f'DELETE FROM persons WHERE username = "{name}"')
        self.db.commit()

    def close_db(self):
        self.db.close()
