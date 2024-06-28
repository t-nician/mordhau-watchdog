import json5

import pymongo

from dataclasses import dataclass, field

import pymongo.collection
import pymongo.database


@dataclass
class PlaytimePlayer:
    playfab: str = field(default="")
    
    total_playtime: int = field(default=0)
    one_week: int = field(default=0)
    two_weeks: int = field(default=0)
    one_month: int = field(default=0)
    

@dataclass
class MongoDBConnection:
    client: None | pymongo.MongoClient = field(default=None)
    
    url: str = field(default="")

    user: str = field(default="")
    password: str = field(default="")
    
    mordhau_database: pymongo.database.Database | None = field(default=None)
    playtime_collection: pymongo.collection.Collection | None = field(default=None)
    
    def __post_init__(self):
        if self.url != "" and self.user != "" and self.password != "":
            self.client = pymongo.MongoClient(
                "mongodb+srv://" + self.url,
                username=self.user,
                password=self.password,
            )
            
            self.mordhau_database = self.client["mordhau"]
            self.playtime_collection = self.mordhau_database["playtime"]

    
    def get_playtime_data(self, playfab: str) -> PlaytimePlayer | None:
        result = None
        
        try:
            result = self.playtime_collection.find({
                "playfab": playfab
            })[0]
        except:
            pass
        
        if result is None:
            return None
        
        return PlaytimePlayer(
            playfab=playfab,
            total_playtime=result.get("total_playtime"),
            one_week=result.get("one_week"),
            two_weeks=result.get("two_weeks"),
            one_month=result.get("one_month")
        )
    
    
    def create_playtime_data(self, playfab: str) -> PlaytimePlayer | None:
        if self.get_playtime_data(playfab) is not None:
            return None
        
        self.playtime_collection.insert_one({
            "playfab": playfab,
            "total_playtime": 0,
            "one_week": 0,
            "two_weeks": 0,
            "one_month": 0
        })
        
        return PlaytimePlayer(
            playfab=playfab,
            total_playtime=0,
            one_week=0,
            two_weeks=0,
            one_month=0
        )
        
    
    
    def save_playtime_player(self, player: PlaytimePlayer):
        self.playtime_collection.update_one(
            {"playfab": player.playfab},
            {"$set": {
                "total_playtime": player.total_playtime,
                "one_week": player.one_week,
                "two_weeks": player.two_weeks,
                "one_month": player.one_month
            }}
        )
        
    

def from_config(path: str) -> MongoDBConnection:
    with open(path, "r") as file:
        config = json5.loads(file.read())
        
        return MongoDBConnection(
            url=config["mongo_url"],
            user=config["mongo_user"],
            password=config["mongo_pass"]
        )