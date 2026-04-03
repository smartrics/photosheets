# PhotoSheets - Automated Photo Download and Print Sheet Creation

PhotoSheets is a collection of Python scripts that automate the process of downloading photos from Google Photos and organizing them into printable PDF sheets with customizable grids. 

## The Story

My daughter studies art and needs to print 10s of photos for her projects. Each photo needs to be arranged in a grid on sheets of paper so she can work on them. Doing this manually is incredibly time-consuming and tedious. These scripts automate the entire workflow:

1. **Interactive photo selection** from Google Photos
2. **Automatic download** of selected photos
3. **Smart organization** into printable PDF sheets with customizable grids
4. **Optimized layout** for cutting the photos for usage

## What's Included

- `download_photos.py` - Downloads photos from Google Photos using the interactive Picker API
- `create_photo_pdfs.py` - Creates PDF sheets with photos arranged in customizable grids
- `requirements.txt` - Python dependencies
- `README_DOWNLOAD.md` - Detailed download script documentation
- `README_PDF.md` - Detailed PDF creation documentation

## Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud Console project with Photos Picker API enabled
- OAuth 2.0 credentials

### Installation

1. Clone this repository:
```bash
git clone https://github.com/smartrics/photosheets.git
cd photosheets
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Photos API credentials (see [README_DOWNLOAD.md](README_DOWNLOAD.md) for detailed instructions)

### Usage

#### Step 1: Download Photos
```bash
python download_photos.py
```
This opens an interactive Google Photos picker where you can select the photos you want to download.

#### Step 2: Create Print Sheets
```bash
python create_photo_pdfs.py
```
Creates PDF files with your downloaded photos arranged in a 3x3 grid (default) on a4-sized pages.

#### Custom Grid Layouts
```bash
# 2x4 grid (8 photos per page)
python create_photo_pdfs.py --cols 2 --rows 4

# 4x2 grid (8 photos per page)
python create_photo_pdfs.py --cols 4 --rows 2

# Single column (great for tall photos)
python create_photo_pdfs.py --cols 1 --rows 5
```

## 📋 Features

### Download Script (`download_photos.py`)
- Interactive Google Photos picker interface
- Secure OAuth2 authentication
- Batch download of selected photos
- Automatic organization in timestamped folders
- Support for up to 200 photos per session

### PDF Creator (`create_photo_pdfs.py`)
- Customizable grid layouts (1-5 columns, 1-4 rows)
- Automatic photo rotation and sizing
- Multi-page PDF support
- High-quality image processing
- A4-sized pages
- Optimized for printing

## Detailed Documentation

- **[Download Script Guide](README_DOWNLOAD.md)** - Complete setup and usage for photo downloading
- **[PDF Creator Guide](README_PDF.md)** - Advanced PDF creation options and customization

## 🐛 Troubleshooting

### Common Issues

**"Access blocked: This app's request is invalid"**
- Check your OAuth consent screen configuration
- Ensure Photos Picker API is enabled in Google Cloud Console

**"No photos found in downloads folder"**
- Make sure you've run the download script first
- Check that photos were successfully downloaded to `downloads_selected_photos/`

**PDF creation fails**
- Verify Pillow and ReportLab are installed: `pip install -r requirements.txt`
- Check that downloaded photos are valid image files

### Getting Help

1. Check the detailed READMEs for your specific script
2. Verify all prerequisites are met
3. Ensure your Google Cloud Console project is properly configured

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
