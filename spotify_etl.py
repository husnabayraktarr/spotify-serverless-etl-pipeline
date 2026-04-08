import os
import json
import csv
import requests
import boto3
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

BUCKET_NAME = "spotify-etl-husna"
RAW_FILE_NAME = "spotify_raw.json"
PROCESSED_FILE_NAME = "spotify_processed.csv"

RAW_S3_KEY = "raw/spotify_raw.json"
PROCESSED_S3_KEY = "processed/spotify_processed.csv"

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env file")


def get_token():
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30
    )
    response.raise_for_status()
    return response.json()["access_token"]


def search_artist(token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": "Drake",
        "type": "artist",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_json(data):
    with open(RAW_FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved local file: {RAW_FILE_NAME}")


def transform_artist_data(raw_data):
    items = raw_data.get("artists", {}).get("items", [])
    if not items:
        raise ValueError("No artist data found in Spotify response.")

    artist = items[0]

    transformed = {
        "artist_name": artist.get("name", ""),
        "artist_id": artist.get("id", ""),
        "popularity": artist.get("popularity", 0),
        "followers": artist.get("followers", {}).get("total", 0),
        "genres": ", ".join(artist.get("genres", [])),
        "spotify_url": artist.get("external_urls", {}).get("spotify", "")
    }

    return transformed


def save_processed_csv(transformed_data):
    with open(PROCESSED_FILE_NAME, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=transformed_data.keys())
        writer.writeheader()
        writer.writerow(transformed_data)

    print(f"Saved local file: {PROCESSED_FILE_NAME}")


def upload_file_to_s3(local_file, s3_key):
    s3 = boto3.client("s3")
    s3.upload_file(local_file, BUCKET_NAME, s3_key)
    print(f"Uploaded to s3://{BUCKET_NAME}/{s3_key}")


def main():
    token = get_token()
    raw_data = search_artist(token)

    save_raw_json(raw_data)
    upload_file_to_s3(RAW_FILE_NAME, RAW_S3_KEY)

    transformed_data = transform_artist_data(raw_data)
    save_processed_csv(transformed_data)
    upload_file_to_s3(PROCESSED_FILE_NAME, PROCESSED_S3_KEY)

    print("Spotify ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()
