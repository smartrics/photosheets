# Google Photos Downloader

This Python script downloads photos from Google Photos to your local machine using the **Google Photos Picker API**. It provides an interactive, secure way to select and download photos without requiring manual album navigation.

## What It Does & Why

This script uses the **Google Photos Picker API** to:
- ✅ **Interactive Selection** - Opens Google Photos UI in your browser
- ✅ **User-Friendly** - Point-and-click photo selection
- ✅ **Secure** - OAuth2 authentication, no password sharing
- ✅ **Full Library Access** - Browse your entire Google Photos library
- ✅ **Batch Downloads** - Select multiple photos at once
- ✅ **Token Caching** - Reuses credentials for repeat runs (no re-auth needed)
- ✅ **Full Resolution** - Downloads original quality images

## How It Works

1. **Authentication** - Creates secure OAuth connection to Google Photos (first time only)
2. **Picker Session** - Opens an interactive picker UI in your browser
3. **Selection** - You select the photos you want via the familiar Google Photos interface
4. **Download** - All selected photos are downloaded to `./downloads_selected_photos/`
5. **Session Cleanup** - Securely closes the session

## Prerequisites

- Python 3.6 or higher
- A Google Cloud Project with Google Photos API enabled
- OAuth 2.0 credentials (`.credentials.json`)
- macOS, Linux, or Windows

## Setup (One-Time)

### 1. Create a Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project (or use an existing one)

### 2. Enable Google Photos API
- Go to **APIs & Services** > **Library**
- Search for "Google Photos Library API"
- Click **Enable**

### 3. Create OAuth 2.0 Credentials
- Go to **APIs & Services** > **Credentials**
- Click **+ Create Credentials** > **OAuth 2.0 Client IDs**
- Choose **Desktop application** as the type
- Download the JSON file
- Rename it to `.credentials.json`
- Place it in the same directory as `download_photos.py`

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Default)
```bash
python download_photos.py
```

The script will:
1. Authenticate with Google (first run only; reuses `token.json` on subsequent runs)
2. Open a browser with the Google Photos picker UI
3. You select photos in the picker
4. Once done, close the picker tab or complete the selection
5. Photos download to `./downloads_selected_photos/`

### Optional: Help Text
```bash
python download_photos.py --help
```

## Features Explained

### OAuth2 Authentication
- **First Run**: Opens browser for authorization. Grants read-only access to Google Photos
- **Token Caching**: Saves credentials in `token.json` for future use
- **Scope**: `photospicker.mediaitems.readonly` - allows reading selected media items only
- **No Password Stored**: Uses secure OAuth flow, your password is never shared

### Interactive Picker
- Browse your entire Google Photos library
- Search, filter, and select photos
- Multi-selection support (select multiple photos at once)
- Maximum 200 photos per session
- Works with all Google Photos features (albums, search, favorites, etc.)

### Automatic Cleanup
- Sessions are properly deleted after use
- Token automatically refreshes when expired
- Handles network interruptions gracefully

## Output

Created directory: `./downloads_selected_photos/`
- Contains all selected photos in original resolution
- Filenames preserved from Google Photos
- Organized by date (Google Photos default naming)

## Limitations & Notes

- **Photos Only**: Currently downloads photos (not videos)
- **Resolution**: Downloads at full original resolution (may be large)
- **Session Timeout**: Default 10-minute timeout for selection
- **Authentication**: Each unique Google account needs separate authorization
- **Network**: Requires stable internet connection throughout

## Troubleshooting

### "Credentials file '.credentials.json' not found"
- Download OAuth credentials from Google Cloud Console
- Rename to `.credentials.json`
- Place in same directory as script

### "Request had insufficient authentication scopes"
- Delete `token.json`
- Re-run to re-authenticate with correct scopes
- This happens if scope changed

### "Timed out waiting for user selection"
- The picker was left open beyond 10 minutes without completing selection
- Restart the script and complete selection faster

### "Failed to download [filename]"
- Network interruption or Google Photos API error
- Script logs errors but continues with other photos
- Check internet connection and try again

### OAuth Verification Screen
- First time may show "unverified app" warning
- This is normal for personal OAuth apps
- Click through the warning to proceed

## Integration with Photo Downloader Workflow

This script is part of a workflow:
1. **download_photos.py** ← You are here (select & download photos)
2. **create_photo_pdfs.py** ← Next step (arrange into PDF galleries)

## Advanced Tips

### Batch Processing
- Download different photo sets at different times
- Each run appends to `./downloads_selected_photos/`
- Or move downloaded photos to separate folders between runs

### Token Management
- `token.json` contains your refresh token
- Keep it safe, don't share it
- Delete it to force re-authentication
- It's tied to the specific Google account and credentials

### Custom Parameters
- Optional `--grid` parameter (for future extension)
- See code comments for other internal options

## Security Considerations

- ✅ Uses OAuth2 (industry standard)
- ✅ Token saved locally (not transmitted)
- ✅ Credentials file never uploaded
- ✅ Session automatically deleted after use
- ❌ Don't share `.credentials.json` or `token.json`
- ❌ Keep Google Cloud project credentials private
