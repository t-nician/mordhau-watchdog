import peewee

database_connection = peewee.SqliteDatabase("./database.sqlite")
database_connection.connect()


class BaseModel(peewee.Model):
    class Meta:
        database = database_connection
        
        
class Playtime(BaseModel):
    playfab_id = peewee.TextField(index=True, unique=True, primary_key=True)
    playtime = peewee.FloatField(default=0)


TABLES = [Playtime]

for table in TABLES:
    if not database_connection.table_exists(table):
        database_connection.create_tables([table])
        database_connection.commit()