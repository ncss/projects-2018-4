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
        ''', (ID,))
        for row in cur:
            cur.close()
            return Category(row[0], row[1], row[2], row[3])
        cur.close()
        return None

    @staticmethod
    def create_category(self,image, name , information):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        allcat = get_categories(conn)
        maxid = 0
        for category in allcat:
            if Category.ID > maxid:
                maxid = Category.ID
        maxid += 1
        cur.execute('''
        INSERT INTO category VALUES (?,?,?,?)
        '''(maxid,image,information,name))
        cur.close()


class Meme:
    _conn = sqlite3.connect('db/main.db')

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
    def create_meme_post(image, caption, latitude, longitude, unsername, timestamp, catid):
        conn = sqlite3.connect('db/main.db')
        cur = conn.cursor()
        allmemes = get_memes_for_category(conn)
        maxid = 0
        for meme in allmemes:
            if Meme.ID > maxid:
                maxid = Meme.ID
        maxid += 1
        cur.execute('''
        INSERT INTO category VALUES (?,?,?,?,?,?,?,?)
        '''(maxid,image,caption,latitude, longitude,username,timestamp,catid))
        cur.close()
