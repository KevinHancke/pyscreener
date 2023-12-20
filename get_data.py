import yfinance as yf
import pandas as pd
from datetime import timedelta, datetime
from database import engine

def get_new_rows(engine):
    df = yf.download("BTC-USD", start=pd.to_datetime("today")-timedelta(7), interval="1m")
    #df_timestamp = df.index[0].tz_localize(None)
    max_date_str = pd.read_sql("SELECT MAX(Datetime) FROM btc_1m", engine).values[0][0]
    max_date_timestamp = pd.to_datetime(max_date_str, utc=df.index.tzinfo)
    #max_date_timestamp = pd.to_datetime(max_date_str).tz_localize(None)
    new_rows = df[df.index> max_date_timestamp]
    return new_rows

def append_new_rows(engine):
    new_rows = get_new_rows(engine)
    new_rows.to_sql("btc_1m", engine, if_exists="append")
    print(str(len(new_rows)) + "rows have been imported")

"""async def get_new_rows():
#I get the old db from the existing sql db
    try:
        db = pd.read_sql('SELECT * FROM BTCUSD_1m', engine)
    except Exception as e:
        # Handle the error (e.g., create the table if it doesn't exist)
        print(f"Error reading data from the sql database: {e}")
        db = pd.DataFrame()

# We get the new data of the last 7 days in a pd dataframe
    df = yf.download('BTC-USD', start=pd.to_datetime('today') - timedelta(7), interval="1m")

    try:
        max_date = pd.read_sql('SELECT MAX(Datetime) FROM BTCUSD_1m', engine).values[0][0]
    except Exception as e:
        print(f"Error getting max date from the database: {e}")
        max_date = pd.to_datetime('today') - timedelta(7)

    
     # Convert max_date to NumPy datetime64[ns] if necessary
    max_date = pd.to_datetime(max_date).to_datetime64()

    # Convert entire DataFrame index to timestamps
    #df_timestamps = pd.to_datetime(df.index)

    # Filter new_rows based on the condition
    new_rows = df[df.index > max_date]
    

    print(f"Max Date: {max_date}")
    print(f"Number of New Rows: {len(new_rows)}")
    print(f"New Rows Head:\n{new_rows.head()}")
    print(f"Data types of new rows: {df.index.dtype}")
    print(f"Data types of db: {db.index.dtype}")


# We try to append the new rows to the database
    try:
        new_rows.to_sql('BTCUSD_1m', engine, if_exists='append', index=False)
        
    except Exception as e:
        print(f"Error writing data to the database: {e}")
    ""
    print(f"I am the new db and I should contain new rows: {db}")"""


"""import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from datetime import timedelta, timezone
from database import engine
from models import ItemDB
from sqlalchemy import func

def get_rows(db: Session):
    try:
        db_data = pd.read_sql('SELECT * FROM BTCUSD_1m', engine)
    except Exception as e:
        # Handle the error (e.g., create the table if it doesn't exist)
        print(f"Error reading data from the database: {e}")
        db_data = pd.DataFrame()

    df = yf.download('BTC-USD', start=pd.to_datetime('today') - timedelta(7), interval="1m")

    try:
        max_date_result = (
            db.query(func.max(ItemDB.Datetime).label("max_date"))
            .first()
        )
        max_date = max_date_result.max_date if max_date_result else None
        if max_date:
            if max_date.tzinfo:
                # Convert to regular datetime, assuming UTC
                max_date = max_date.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                # Already a regular datetime
                max_date = max_date
        else:
            max_date = pd.to_datetime('today') - timedelta(7)
    except Exception as e:
        # Handle the error (e.g., set max_date to a default value)
        print(f"Error getting max date from the database: {e}")
        max_date = pd.to_datetime('today') - timedelta(7)

    new_rows = df[df.index > max_date]

    try:
        for _ , row in new_rows.iterrows():
            db_item = ItemDB(**row.to_dict())
            db.add(db_item)
        db.commit()
    except Exception as e:
        # Handle the error (e.g., print an error message)
        print(f"Error writing data to the database: {e}")

    return db_data"""


"""def getRows():
    try:
        db = pd.read_sql('SELECT * FROM BTCUSD_1m', engine)
    except Exception as e:
        # Handle the error (e.g., create the table if it doesn't exist)
        print(f"Error reading data from the database: {e}")
        db = pd.DataFrame()

    df = yf.download('BTC-USD', start=pd.to_datetime('today') - timedelta(7), interval="1m")

    try:
        max_date = pd.read_sql('SELECT MAX(Datetime) FROM BTCUSD_1m', engine).values[0][0]
    except Exception as e:
        # Handle the error (e.g., set max_date to a default value)
        print(f"Error getting max date from the database: {e}")
        max_date = pd.to_datetime('today') - timedelta(7)

    new_rows = df[df.index > max_date]

    try:
        new_rows.to_sql('BTCUSD_1m', engine, if_exists='append', index=False)
    except Exception as e:
        # Handle the error (e.g., print an error message)
        print(f"Error writing data to the database: {e}")

    return db
"""