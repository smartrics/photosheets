#!/usr/bin/env python3

import os
import sys
import time
import requests

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/photospicker.mediaitems.readonly"]
CLIENT_SECRETS_FILE = "./.credentials.json"
TOKEN_FILE = "token.json"


def authenticate():
    creds = None

    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"ERROR: Credentials file '{CLIENT_SECRETS_FILE}' not found.")
        sys.exit(1)

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            saved_scopes = set(creds.scopes or [])
            if not set(SCOPES).issubset(saved_scopes):
                print("INFO: Saved credentials do not include required scopes. Reauthenticating...")
                creds = None
        except Exception as e:
            print(f"WARNING: Failed to load existing token file '{TOKEN_FILE}': {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds


def create_picker_session(photospicker_service):
    session_request = {
        "pickingConfig": {
            "maxItemCount": 200
        }
    }
    return photospicker_service.sessions().create(body=session_request).execute()


def parse_duration_to_seconds(value: str) -> float:
    if not value:
        return 2.0

    value = value.strip().lower()

    if value.endswith("ms"):
        return float(value[:-2]) / 1000.0
    if value.endswith("s"):
        return float(value[:-1])

    raise ValueError(f"Unsupported duration format: {value}")


def wait_for_user_selection(photospicker_service, session_id, timeout_seconds=600):
    start = time.time()

    while True:
        session = photospicker_service.sessions().get(sessionId=session_id).execute()

        if session.get("mediaItemsSet"):
            return session

        polling = session.get("pollingConfig", {})
        poll_interval = polling.get("pollInterval", "2s")
        sleep_seconds = parse_duration_to_seconds(poll_interval)

        if time.time() - start > timeout_seconds:
            raise TimeoutError("Timed out waiting for the user to finish picking media items.")

        time.sleep(sleep_seconds)


def list_picked_media_items(photospicker_service, session_id):
    items = []
    page_token = None

    while True:
        kwargs = {"sessionId": session_id, "pageSize": 100}
        if page_token:
            kwargs["pageToken"] = page_token

        resp = photospicker_service.mediaItems().list(**kwargs).execute()
        items.extend(resp.get("mediaItems", []))

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return items


def safe_filename(name):
    return "".join(c for c in name if c not in '/\\\0').strip() or "downloaded_file"


def download_picked_media_items(media_items, download_dir, creds):
    os.makedirs(download_dir, exist_ok=True)

    if not media_items:
        print("No media items selected.")
        return

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    headers = {"Authorization": f"Bearer {creds.token}"}

    for item in media_items:
        media_file = item.get("mediaFile", {})
        base_url = media_file.get("baseUrl")
        filename = media_file.get("filename") or item.get("id") or "downloaded_file"

        if not base_url:
            print(f"Skipping item without baseUrl: {item.get('id', '<unknown>')}")
            continue

        download_url = base_url + "=d"
        filepath = os.path.join(download_dir, safe_filename(filename))

        print(f"Downloading {filename}...")

        try:
            response = requests.get(download_url, headers=headers, timeout=120)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")


def delete_session(photospicker_service, session_id):
    try:
        photospicker_service.sessions().delete(sessionId=session_id).execute()
    except Exception as e:
        print(f"WARNING: Failed to delete session {session_id}: {e}")


def main():
    download_dir = "downloads_selected_photos"

    album_name = sys.argv[1] if len(sys.argv) > 1 else None

    creds = authenticate()
    photospicker_service = build("photospicker", "v1", credentials=creds, static_discovery=False)

    try:
        session = create_picker_session(photospicker_service)
        session_id = session["id"]
        picker_uri = session["pickerUri"]

        print("Open this URL in your browser and complete selection:")
        print(picker_uri)

        if album_name:
            print(f"\nNOTE: Navigate to album '{album_name}' manually in the picker.\n")

        wait_for_user_selection(photospicker_service, session_id)
        media_items = list_picked_media_items(photospicker_service, session_id)
        download_picked_media_items(media_items, download_dir, creds)

        print(f"All selected photos downloaded to {download_dir}")

    except HttpError as e:
        print(f"HTTP error: {e}")
        sys.exit(1)
    except TimeoutError as e:
        print(str(e))
        sys.exit(1)
    finally:
        if "session_id" in locals():
            delete_session(photospicker_service, session_id)


if __name__ == "__main__":
    main()