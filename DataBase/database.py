from peewee import *

database = SqliteDatabase('DataBase/db/library.db')


class BaseModel(Model):
    class Meta:
        database = database


class BookModel(BaseModel):
    book_id = AutoField()
    title = CharField()
    author = CharField()
    description = CharField()
    genre = CharField()


database.connect()
BookModel.create_table()
