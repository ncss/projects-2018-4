import sqlite3
conn = sqlite3.connect('main.db')
cur = conn.cursor()
class Category:
    def __init__(self, ID, image, information, name):
        self.ID = ID
        self.image = image
        self.information = information
        self.name = name

    def get_categories(conn):
        cur = conn.cursor()
        cur.execute('''
        select *
        from category
        where category is not null
        ''')
        categories = []
        for row in cur:
            categories.append(Category(row[0], row[1], row[2], row[3]))
        return categories
            
    def get_category_by_id(conn, ID):
        cur = conn.cursor()
        cur.execute('''
        select *
        from category
        where id = ?
        ''', (ID,))
        for row in cur:
            return Category(row[0], row[1], row[2], row[3])
        return None

    def create_category(conn, image, name , information):
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


class Memes:
    def __init__(self, ID, image, caption, location, username, timestamp, catid):
        self.ID = ID
        self.image = image
        self.caption = caption
        self.location = location
        self.username = username
        self.timestamp = timestamp
        self.catid = catid

    def get_memes_for_category(conn, catid):
        cur = conn.cursor()
        cur.execute('''
        select *
        from memes m
        where catid == ?
        '''(catid,))
        memesofcat = []
        for row in cur:
            memesofcat.append(Memes(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return memesofcat

    def create_meme_post(conn, image, caption, location, unsername, timestamp, catid):
        cur = conn.cursor()
        allmemes = get_memes_for_category(conn)
        maxid = 0
        for meme in allmemes:
            if Memes.ID > maxid:
                maxid = Memes.ID
        maxid += 1
        cur.execute('''
        INSERT INTO category VALUES (?,?,?,?,?,?,?)
        '''(maxid,image,caption,location,username,timestamp,catid))
        
