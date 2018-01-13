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
        '''(image,information,name))
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
        ''',(catid,))
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
        INSERT INTO memes (image, caption, locationlat, locationlon, username, timestamp, catid) VALUES (?,?,?,?,?,?,?)
        ''', (image,caption,latitude, longitude,username,timestamp,catid))
        conn.commit()
        lastid = cur.lastrowid
        conn.close()
        return lastid
