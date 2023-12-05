import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        
        CURSOR.execute(sql)
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        
        CURSOR.execute(sql, (self.name, self.breed))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog =  cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog_rows_result = CURSOR.execute(sql, (name,)).fetchone()

        return None if dog_rows_result is None else cls.new_from_db(dog_rows_result)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog_row = CURSOR.execute(sql, (id,)).fetchone()

        return cls.new_from_db(dog_row)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT *
            FROM dogs
            WHERE NAME = ? AND breed = ?
            LIMIT 1
        """
        
        result = CURSOR.execute(sql, (name, breed)).fetchone()
        
        if(result is None):
            dog = Dog.create(name, breed)
            return dog
        else:
            return Dog.new_from_db(result)
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
            breed = ?
            WHERE id = ? 
        """
        
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()