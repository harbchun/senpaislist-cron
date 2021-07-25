import os
import boto3
from sqlalchemy import create_engine
from dotenv import load_dotenv
from utils import times

load_dotenv()

# AWS variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_REGION = os.getenv('AWS_BUCKET_REGION')
AWS_DATA_BUCKET_NAME = os.getenv('AWS_DATA_BUCKET_NAME')
AWS_BROADCAST_TIMES_BUCKET_NAME = os.getenv('AWS_BROADCAST_TIMES_BUCKET_NAME')

# SQL
SQL_HOST = os.getenv('SQL_HOST')
SQL_PORT = os.getenv('SQL_PORT')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_DBNAME = os.getenv('SQL_DBNAME')

# Other
YEAR = times.get_current_year()
SEASON = times.get_current_season()

def main():
    conn_str = 'postgresql+psycopg2://%s:%s@%s:%s:%s' \
        % (SQL_USER, SQL_PASSWORD, SQL_HOST, SQL_PORT, SQL_DBNAME)
    engine = create_engine(conn_str)
    connection = engine.connect()

    # AWS
    s3 = boto3.resource(
        's3', 
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_BUCKET_REGION,
    )
    data_bucket = s3.Bucket(AWS_DATA_BUCKET_NAME)
    data_objects = data_bucket.objects.filter(Prefix=str(YEAR)+'/'+SEASON)

if __name__ == '__main__':
    main()