# Photo PDF Gallery Creator

This script creates professional PDF documents with customizable photo grid layouts from images downloaded by the photo downloader.

## Features

- **A4 Landscape** page orientation
- **Customizable grid layout** - default 3x3 (supports 1-5 columns, 1-4 rows)
- **Automatic portrait handling** - rotates portrait images 90° clockwise
- **Smart resizing** - maintains aspect ratio while fitting grid cells
- **Professional spacing** - 20px page borders, 5px padding between photos
- **High quality output** - 300 DPI (suitable for printing)
- **Flexible output modes**:
  - Single PDF with all photos (default)
  - Multiple PDFs split by grid (one grid per PDF)
- **Original photos preserved** - source files remain unchanged

## Setup

1. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure you have downloaded photos using `download_photos.py`

## Usage

### Default: Single PDF with 3x3 grid
```bash
python create_photo_pdfs.py
```
Creates: `photo_pdfs/gallery.pdf`

### Single PDF with custom grid size
```bash
python create_photo_pdfs.py --grid 2x2   # 4 photos per page
python create_photo_pdfs.py --grid 4x3   # 12 photos per page
python create_photo_pdfs.py --grid 5x4   # 20 photos per page (maximum)
```

### Split into multiple PDFs
```bash
python create_photo_pdfs.py --split
```
Creates: `photo_pdfs/gallery_001.pdf`, `gallery_002.pdf`, etc. (9 photos each with 3x3 grid)

### Split with custom grid size
```bash
python create_photo_pdfs.py --grid 2x2 --split   # Creates PDFs with 4 photos each
python create_photo_pdfs.py --grid 4x2 --split   # Creates PDFs with 8 photos each
```

### View all options
```bash
python create_photo_pdfs.py --help
```

## Page Layout

- **Page Size**: A4 Landscape (297mm × 210mm)
- **Borders**: 20px on all sides
- **Padding**: 5px between photos
- **Photo Rotation**: Portrait images automatically rotated 90° clockwise
- **Aspect Ratio**: Preserved for all photos
- **Grid Options**: 1-5 columns × 1-4 rows

## Grid Size Reference

| Grid | Photos | Use Case |
|------|--------|----------|
| 1x1 | 1 | Single photo per page |
| 2x2 | 4 | Smaller, more detailed view |
| 3x3 | 9 | Default, balanced layout |
| 4x3 | 12 | More photos, compact |
| 5x4 | 20 | Maximum density |

## Output

- **PDF Files**: `photo_pdfs/gallery.pdf` or `gallery_001.pdf`, `gallery_002.pdf`, etc.
- **Source Photos**: `downloads_selected_photos/` (untouched)

## Examples

Process 65 photos into:
- **Single 3x3 PDF**: `python create_photo_pdfs.py` → 1 PDF with all 65 grids
- **Multiple 3x3 PDFs**: `python create_photo_pdfs.py --split` → 8 PDFs
- **Single 5x4 PDF**: `python create_photo_pdfs.py --grid 5x4` → 1 PDF
- **Multiple 2x2 PDFs**: `python create_photo_pdfs.py --grid 2x2 --split` → 17 PDFs

## Notes

- Photos are sorted alphabetically by filename
- Original files are preserved (not deleted or moved)
- If a photo fails to process, the script continues with others and reports errors
- The script displays grid size in the output header
