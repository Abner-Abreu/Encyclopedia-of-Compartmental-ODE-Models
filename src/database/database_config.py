from peewee import SqliteDatabase
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'encyclopedia.db')

db = SqliteDatabase(DB_PATH, pragmas={
    'journal_mode': 'wal',
    'cache_size': -64000,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
})

def init_db():
    db.connect()
    from . import (
        Model, Compartment, Param, Article, 
        Situation, Data,
        ModelCompartment, ModelParam, 
        ModelArticle, ModelSituation, ModelData
    )
    db.create_tables([
        Model, Compartment, Param, Article, 
        Situation, Data,
        ModelCompartment, ModelParam, 
        ModelArticle, ModelSituation, ModelData
    ])
    return db