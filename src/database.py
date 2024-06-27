import peewee

database = peewee.SqliteDatabase("./database.sqlite")
database.connect()


class BaseModel(peewee.Model):
    class Meta:
        database = database
        
        
class PlayerModel(BaseModel):
    playfab = peewee.Field(index=True,primary_key=True,unique=True)
    
    total_playtime = peewee.Field(default="")
    one_week_playtime = peewee.Field(default="")
    two_week_playtime = peewee.Field(default="")
    one_month_playtime = peewee.Field(default="")


def get_playtime_model(playfab: str) -> PlayerModel | None:
    result = None
    
    try:
        result = PlayerModel.get(
            PlayerModel.playfab==playfab
        )
    except:
        pass
    
    return result


def create_playtime_model(playfab: str) -> PlayerModel | None:
    if get_playtime_model(playfab):
        return None
    
    return PlayerModel.create(
        playfab=playfab,
        total_playtime="0",
        one_week_playtime="0",
        two_week_playtime="0",
        one_month_playtime="0"
    )


if not database.table_exists(PlayerModel):
    database.create_tables([PlayerModel])
    database.commit()
