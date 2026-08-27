""" config """
import os

# db connection string either Cloud SQL or MySQL URL
DB_URL = os.getenv("DB_URL", "mysql://root@localhost/devdb")

# optional, build DB_URL from components
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "3306")
if not os.getenv("DB_URL"):
    DB_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
# asset source
# local or cloud
# - local uses the local filesystem, 
# - cloud uses a bucket
ASSET_BACKEND = os.getenv("ASSET_BACKEND", "local").lower()
    # used when local
ASSET_BUCKET = os.getenv("ASSET_BUCKET")
# public URL for assets (optional, used for cloud)
ASSET_PUBLIC_URL = os.getenv("ASSET_PUBLIC_URL", "")

# flask app port
PORT = int(os.getenv("PORT", "8080"))