import duckdb as db
import pandas as pd

file_path = "ManaBox_Collection.csv"

pandas_bozo = pd.read_csv(file_path)

conn = db.connect()

conn.sql(
    """ 
    select trim("Binder Name") as binder, 
        "Binder Type" as btype ,
        "Name" as name, 
        "Set code" as set_code, 
        "Set name" as set_name,
        "Collector number" as col_num, 
        "Foil" as foil, 
        "Rarity" as rarity,
        "Quantity" as quantity, 
        "Scryfall ID" as scryfall_id,
        "Language" as language
    from pandas_bozo
    """
).write_csv('db/collection_fixed.csv')


