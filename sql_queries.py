import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('aws.cfg')

LOG_DATA = config['S3']['LOG_DATA']
LOG_JSON_PATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config.get("S3", "SONG_DATA")
ROLE_ARN = config['IAM']['DWH_ARN']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplays;"
user_table_drop = "DROP TABLE IF EXISTS dim_users;"
song_table_drop = "DROP TABLE IF EXISTS dim_songs;"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists;"
time_table_drop = "DROP TABLE IF EXISTS dim_datetime;"

# CREATE TABLES

# Create staging tables
staging_events_table_create = ("""
    CREATE TABLE staging_events(
        artist              VARCHAR,
        auth                VARCHAR,
        firstName           VARCHAR,
        gender              VARCHAR,
        itemInSession       INTEGER,
        lastName            VARCHAR,
        length              FLOAT,
        level               VARCHAR,
        location            VARCHAR,
        method              VARCHAR,
        page                VARCHAR,
        registration        FLOAT,
        sessionId           INTEGER,
        song                VARCHAR,
        status              INTEGER,
        ts                  TIMESTAMP,
        userAgent           VARCHAR,
        userId              INTEGER 
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs(
        num_songs           INTEGER,
        artist_id           VARCHAR,
        artist_latitude     FLOAT,
        artist_longitude    FLOAT,
        artist_location     VARCHAR,
        artist_name         VARCHAR,
        song_id             VARCHAR,
        title               VARCHAR,
        duration            FLOAT,
        year                INTEGER
    )
""")

# Create Songplay Fact table
songplay_table_create = ("""
    CREATE TABLE fact_songplays(
        songplay_id         INTEGER         IDENTITY(0,1)   PRIMARY KEY SORTKEY DISTKEY,
        start_time          TIMESTAMP       NOT NULL,
        user_id             INTEGER         NOT NULL,
        level               VARCHAR,
        song_id             VARCHAR         NOT NULL,
        artist_id           VARCHAR         NOT NULL,
        session_id          INTEGER,
        location            VARCHAR,
        user_agent          VARCHAR
    )
""")

# Create User Dimension table
user_table_create = ("""
    CREATE TABLE dim_users(
        user_id             INTEGER         NOT NULL PRIMARY KEY DISTKEY,
        first_name          VARCHAR         NOT NULL,
        last_name           VARCHAR         NOT NULL,
        gender              VARCHAR         NOT NULL,
        level               VARCHAR         NOT NULL
    )
""")

# Create Song Dimension table
song_table_create = ("""
    CREATE TABLE dim_songs(
        song_id             VARCHAR         NOT NULL  PRIMARY KEY SORTKEY,
        title               VARCHAR         NOT NULL,
        artist_id           VARCHAR         NOT NULL DISTKEY,
        year                INTEGER         NOT NULL,
        duration            FLOAT
    )
""")

# Create Artist Dimension table
artist_table_create = ("""
    CREATE TABLE dim_artists(
        artist_id           VARCHAR         NOT NULL  PRIMARY KEY DISTKEY,
        name                VARCHAR         NOT NULL,
        location            VARCHAR,
        latitude            FLOAT,
        longitude           FLOAT
    )
""")

# Create Datetime Dimension table
time_table_create = ("""
    CREATE TABLE dim_datetime(
        start_time          TIMESTAMP       NOT NULL DISTKEY SORTKEY PRIMARY KEY,
        hour                INTEGER         NOT NULL,
        day                 INTEGER         NOT NULL,
        week                INTEGER         NOT NULL,
        month               INTEGER         NOT NULL,
        year                INTEGER         NOT NULL,
        weekday             VARCHAR(20)     NOT NULL
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2' 
    FORMAT as JSON {}
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    TIMEFORMAT as 'epochmillisecs';
""").format(LOG_DATA, ROLE_ARN, LOG_JSON_PATH)

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2' 
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    FORMAT as JSON 'auto';
""").format(SONG_DATA, ROLE_ARN)

# FINAL TABLES

# FACTS TABLES
songplay_table_insert = ("""
    INSERT INTO fact_songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT  DISTINCT(events.ts)  AS start_time, 
            events.userId        AS user_id, 
            events.level         AS level, 
            songs.song_id       AS song_id, 
            songs.artist_id     AS artist_id, 
            events.sessionId     AS session_id, 
            events.location      AS location, 
            events.userAgent     AS user_agent
    FROM staging_events events
    JOIN staging_songs  songs   
        ON events.song = songs.title AND events.artist = songs.artist_name
    AND events.page  =  'NextSong'
""")

# DIMENSION TABLES

# user dimension table
user_table_insert = ("""
    INSERT INTO dim_users (user_id, first_name, last_name, gender, level)
    SELECT  DISTINCT(userId)    AS user_id,
            firstName           AS first_name,
            lastName            AS last_name,
            gender,
            level
    FROM staging_events
    WHERE user_id IS NOT NULL
    AND page  =  'NextSong';
""")

# song dimension table
song_table_insert = ("""
    INSERT INTO dim_songs (song_id, title, artist_id, year, duration)
    SELECT  DISTINCT(song_id) AS song_id,
            title,
            artist_id,
            year,
            duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
""")

# artist dimension table
artist_table_insert = ("""
    INSERT INTO dim_artists (artist_id, name, location, latitude, longitude)
    SELECT  DISTINCT(artist_id) AS artist_id,
            artist_name         AS name,
            artist_location     AS location,
            artist_latitude     AS latitude,
            artist_longitude    AS longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

# datetime dimension table
datetime_table_insert = ("""
    INSERT INTO dim_datetime (start_time, hour, day, week, month, year, weekday)
    SELECT  DISTINCT(start_time)                AS start_time,
            EXTRACT(hour FROM start_time)       AS hour,
            EXTRACT(day FROM start_time)        AS day,
            EXTRACT(week FROM start_time)       AS week,
            EXTRACT(month FROM start_time)      AS month,
            EXTRACT(year FROM start_time)       AS year,
            EXTRACT(dayofweek FROM start_time)  as weekday
    FROM fact_songplays;
""")


# GET NUMBER OF ROWS IN EACH TABLE
get_number_staging_events = ("""
    SELECT COUNT(*) FROM staging_events
""")

get_number_staging_songs = ("""
    SELECT COUNT(*) FROM staging_songs
""")

get_number_songplays = ("""
    SELECT COUNT(*) FROM fact_songplays
""")

get_number_users = ("""
    SELECT COUNT(*) FROM dim_users
""")

get_number_songs = ("""
    SELECT COUNT(*) FROM dim_songs
""")

get_number_artists = ("""
    SELECT COUNT(*) FROM dim_artists
""")

get_number_time = ("""
    SELECT COUNT(*) FROM dim_datetime
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create,
                        user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert,
                        datetime_table_insert]
select_number_rows_queries = [get_number_staging_events, get_number_staging_songs, get_number_songplays,
                              get_number_users, get_number_songs, get_number_artists, get_number_time]
