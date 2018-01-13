import sqlite3

class Category:
    def __init__(self, ID = None, image = None, information = None, name = None):
        self.ID = ID
        self.image = image
        self.information = information
        self.name = name

    @staticmethod
    def get_categories():
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        select *
        from Category;
        ''')
        categories = []
        for row in cur:
            categories.append(Category(row[0], row[1], row[2], row[3]))
        cur.close()
        return categories

    @staticmethod
    def get_category_by_id(ID):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        select *
        from category
        where id = ?;
        ''', ID)
        for row in cur:
            cur.close()
            return Category(row[0], row[1], row[2], row[3])
        cur.close()
        return None

    @staticmethod
    def create_category(self,image, name , information):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO category (image, information, name) VALUES (?,?,?)
        '''(image,information,name)) #Must be a tuple. do not delete the brackets or comma
        conn.commit()
        cur.close()
        conn.close()


class Meme:
    def __init__(self, ID = None, image = None, caption = None, latitude = None, longitude = None, username = None, timestamp = None, catid = None):
        self.ID = ID
        self.image = image
        self.caption = caption
        self.latitude = latitude
        self.longitude = longitude
        self.username = username
        self.timestamp = timestamp
        self.catid = catid

    @staticmethod
    def get_memes_for_category(catid):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        select *
        from memes m
        where catid == ?
        order by id desc
        ''',(catid,)) # Dont' remove the comma in (catid,), since this must be a tuple.
        memesofcat = []
        for row in cur:
            memesofcat.append(Meme(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        cur.close()
        return memesofcat

    @staticmethod
    def create_meme_post(image, caption, latitude, longitude, username, timestamp, catid):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO memes (image, caption, locationlat, locationlon, userid, timestamp, catid) VALUES (?,?,?,?,?,?,?)
        ''', (image,caption,latitude, longitude,username,timestamp,catid)) #Must be a tuple. do not delete the brackets or comma
        conn.commit()
        lastid = cur.lastrowid
        conn.close()
        return lastid


class Person:
    def __init__(self, id = None, password = None, name = None, bio = None, image = None):
        self.id = id
        self.password = password
        self.name = name
        self.bio = bio
        self.image = image

    @staticmethod
    def get_user_by_id(id):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        select *
        from person
        where id = ?;
        ''', (id,)) #Must be a tuple. do not delete the brackets or comma
        for row in cur:
            cur.close()
            return Person(row[0], row[1], row[2], row[3], row[4])
        cur.close()
        return None

    @staticmethod
    def get_user_by_username(name):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        select *
        from person
        where name = ?;
        ''', (name,)) #Must be a tuple. do not delete the brackets or comma
        for row in cur:
            cur.close()
            return Person(row[0], row[1], row[2], row[3])
        cur.close()
        return None

    @staticmethod
    def create_user(password, name, bio, image):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO person (password, name, bio, image) VALUES (?,?,?,?)
        ''', (password, name, bio, image))
        conn.commit()
        lastid = cur.lastrowid
        conn.close()
        return lastid
