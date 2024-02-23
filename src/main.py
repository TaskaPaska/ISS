import requests
import time
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import psycopg2
import os
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)


cur = conn.cursor()

last_timestamp = int(time.time())
first_timestamp = last_timestamp - 59  # 60
current_timestamp = first_timestamp

while current_timestamp <= last_timestamp:
    url = f"https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={current_timestamp}"
    # Fetch the data from the API
    response_API = requests.get(url)
    data = response_API.json()
    # print(data)
    df = pd.DataFrame(data)
    # print(df)

    # Convert the 'timestamp' column to a Pandas datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Extract minute, hour, and day information from the timestamp
    df['minute'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    df['hour'] = df['timestamp'].dt.strftime('%Y-%m-%d %H')
    df['day'] = df['timestamp'].dt.strftime('%Y-%m-%d')

    # Convert the 'timestamp' column to a Pandas datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Convert the 'timestamp' column to a Pandas datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Replace colon (:) with underscore (_) and spaces with underscore (_) in the minute column
    df['minute'] = df['timestamp'].dt.strftime('%Y-%m-%d %H_%M').str.replace(' ', '_')

    # Extract hour and day information from the timestamp
    df['hour'] = df['timestamp'].dt.strftime('%Y-%m-%d %H')
    df['day'] = df['timestamp'].dt.strftime('%Y-%m-%d')

    # Specify the directory for partitioned Parquet files
    output_directory = os.path.join(os.path.dirname(__file__), "partitioned_data")

    # Create the partitioned_data directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Create Parquet files partitioned by minute, hour, and day
    for partition_key in ['minute', 'hour', 'day']:
        partitioned_df = df.groupby(partition_key)
        for key, group in partitioned_df:
            group = group.drop(columns=[partition_key])
            table = pa.Table.from_pandas(group)
            file_path = os.path.join(output_directory, f"{partition_key}={key}.parquet")
            pq.write_table(table, file_path)

    if isinstance(data, list) and len(data) > 0:
        # Extract relevant data from the first item in the list
        item = data[0]
        name = item.get("name")
        id = item.get("id")
        latitude = item.get("latitude")
        longitude = item.get("longitude")
        altitude = item.get("altitude")
        velocity = item.get("velocity")
        visibility = item.get("visibility")
        footprint = item.get("footprint")
        timestamp = pd.to_datetime(item.get("timestamp"), unit="s")
        daynum = item.get("daynum")
        solar_lat = item.get("solar_lat")
        solar_lon = item.get("solar_lon")
        units = item.get("units")
        # Insert the data into the PostgreSQL table
        insert_query = """
        INSERT INTO satellite (satellite_name, satellite_id, latitude, longitude, altitude, velocity, visibility, footprint, timestamp, daynum, solar_lat, solar_lon, units)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        cur.execute(insert_query, (
            name, id, latitude, longitude, altitude, velocity, visibility, footprint, timestamp, daynum, solar_lat, solar_lon, units
        ))
    current_timestamp += 1
    # print(df)

conn.commit()
conn.close()


# # Calculate the elapsed time
# end_time = time.time()
# elapsed_time = end_time - last_timestamp
# print(df)

# print(f"execution time: {elapsed_time} seconds")
