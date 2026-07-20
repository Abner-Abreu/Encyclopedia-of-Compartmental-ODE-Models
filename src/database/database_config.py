from peewee import SqliteDatabase
from platformdirs import user_documents_path

DB_DIR = user_documents_path() / "Encyclopedia Of Compartmental ODE Models"
DB_DIR.mkdir(parents=True,exist_ok=True)
DB_PATH = DB_DIR / 'encyclopedia.db'

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