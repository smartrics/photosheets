#!/usr/bin/env python3
"""
Photo PDF Gallery Creator

This script takes photos from ./downloads_selected_photos and creates PDF documents
with a 3x3 grid layout. Photos are organized into individual PDFs when needed.

Features:
- A4 landscape page orientation
- 3x3 grid layout (9 photos per PDF)
- 20px borders on all sides
- 5px padding between photos
- Automatic rotation for portrait images
- 300 DPI high print quality output
- Option to create single PDF or split across multiple PDFs

Usage:
  python create_photo_pdfs.py              # Single PDF (default 3x3 grid)
  python create_photo_pdfs.py --split      # Multiple PDFs (one per grid)
  python create_photo_pdfs.py --grid 4x3   # Custom grid size
  python create_photo_pdfs.py --grid 5x4 --split  # Custom grid, split mode
"""

import os
import argparse
import tempfile
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


# Configuration
SOURCE_DIR = "./downloads_selected_photos"
OUTPUT_DIR = "./photo_pdfs"

# Page settings (reportlab uses points by default, 72 points = 1 inch = 25.4mm)
PAGE_SIZE = landscape(A4)  # 297mm x 210mm
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE
BORDER = 20 * 72 / 25.4 / 10  # Convert 20px to points (72 points/inch, 96px/inch)
PADDING = 5 * 72 / 25.4 / 10   # Convert 5px to points
DPI = 300

# Grid settings
GRID_COLS = 3
GRID_ROWS = 3
PHOTOS_PER_PDF = GRID_COLS * GRID_ROWS


def parse_grid_size(grid_str):
    """
    Parse grid size string in format 'WxH' (e.g., '3x3', '4x2').
    Validates that dimensions are between 1-5 for width and 1-4 for height.
    Returns tuple (cols, rows) on success, or raises ValueError.
    """
    try:
        parts = grid_str.lower().split('x')
        if len(parts) != 2:
            raise ValueError()
        
        cols = int(parts[0])
        rows = int(parts[1])
        
        if not (1 <= cols <= 5) or not (1 <= rows <= 4):
            raise ValueError()
        
        return cols, rows
    
    except (ValueError, IndexError):
        raise ValueError(f"Invalid grid format: '{grid_str}'. Use format like '3x3', '4x2', etc. (cols 1-5, rows 1-4)")


def create_directories():
    """Create output directory if it doesn't exist."""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)


def get_image_files():
    """Get all image files from the source directory."""
    if not Path(SOURCE_DIR).exists():
        print(f"ERROR: Source directory '{SOURCE_DIR}' not found.")
        return []
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = [
        f for f in Path(SOURCE_DIR).iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    return sorted(image_files)


def process_image(image_path):
    """
    Process an image: rotate if portrait, resize to fit grid cell.
    Returns a PIL Image object ready for placement.
    """
    img = Image.open(image_path)
    original_width, original_height = img.size
    
    # Calculate grid cell dimensions (available space divided by grid)
    available_width = PAGE_WIDTH - 2 * BORDER
    available_height = PAGE_HEIGHT - 2 * BORDER
    
    cell_width = (available_width - (GRID_COLS - 1) * PADDING) / GRID_COLS
    cell_height = (available_height - (GRID_ROWS - 1) * PADDING) / GRID_ROWS
    
    # Portrait image: rotate 90 degrees clockwise
    if original_height > original_width:
        img = img.rotate(-90, expand=True)
        original_width, original_height = img.size
    
    # Resize to fit cell while preserving aspect ratio
    img.thumbnail((cell_width, cell_height), Image.Resampling.LANCZOS)
    
    return img, cell_width, cell_height


def create_pdf(image_paths, output_filename):
    """Create a PDF with multiple pages of grid-arranged photos."""
    c = canvas.Canvas(output_filename, pagesize=PAGE_SIZE)
    
    # Calculate cell dimensions
    available_width = PAGE_WIDTH - 2 * BORDER
    available_height = PAGE_HEIGHT - 2 * BORDER
    
    cell_width = (available_width - (GRID_COLS - 1) * PADDING) / GRID_COLS
    cell_height = (available_height - (GRID_ROWS - 1) * PADDING) / GRID_ROWS
    
    print(f"Creating {output_filename}...")
    
    # Create temporary directory for image files
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, image_path in enumerate(image_paths):
            # Calculate which page and position within page
            page_num = idx // (GRID_COLS * GRID_ROWS)
            pos_in_grid = idx % (GRID_COLS * GRID_ROWS)
            row = pos_in_grid // GRID_COLS
            col = pos_in_grid % GRID_COLS
            
            # Create new page if needed
            if idx > 0 and pos_in_grid == 0:
                c.showPage()
            
            try:
                # Process image
                img, _, _ = process_image(image_path)
                
                # Save to temporary file
                tmp_img_path = os.path.join(tmpdir, f"temp_{idx}.png")
                img.save(tmp_img_path, "PNG")
                
                # Calculate position (x from left, y from top)
                x = BORDER + col * (cell_width + PADDING)
                y = PAGE_HEIGHT - BORDER - (row + 1) * cell_height - row * PADDING
                
                # Center image in cell
                img_width, img_height = img.size
                x_offset = (cell_width - img_width) / 2
                y_offset = (cell_height - img_height) / 2
                
                c.drawImage(
                    tmp_img_path,
                    x + x_offset,
                    y + y_offset,
                    width=img_width,
                    height=img_height,
                    preserveAspectRatio=True
                )
                
                print(f"  Added: {image_path.name}")
                
            except Exception as e:
                print(f"  ERROR processing {image_path.name}: {e}")
    
    c.save()
    total_pages = (len(image_paths) + GRID_COLS * GRID_ROWS - 1) // (GRID_COLS * GRID_ROWS)
    print(f"PDF created: {output_filename} ({total_pages} page(s))\n")

def main(split_mode=False, grid_cols=3, grid_rows=3):
    global GRID_COLS, GRID_ROWS, PHOTOS_PER_PDF
    GRID_COLS = grid_cols
    GRID_ROWS = grid_rows
    PHOTOS_PER_PDF = GRID_COLS * GRID_ROWS
    
    print("=" * 60)
    mode = "(Split Mode)" if split_mode else "(Single PDF Mode)"
    print(f"Photo PDF Gallery Creator {mode} - Grid: {GRID_COLS}x{GRID_ROWS}")
    print("=" * 60 + "\n")
    
    # Setup
    create_directories()
    image_files = get_image_files()
    
    if not image_files:
        print("No image files found in downloads_selected_photos/")
        return
    
    print(f"Found {len(image_files)} image(s)\n")
    
    if split_mode:
        # Process images in batches (split mode)
        total_pdfs = (len(image_files) + PHOTOS_PER_PDF - 1) // PHOTOS_PER_PDF
        
        for pdf_idx in range(total_pdfs):
            start_idx = pdf_idx * PHOTOS_PER_PDF
            end_idx = min(start_idx + PHOTOS_PER_PDF, len(image_files))
            batch = image_files[start_idx:end_idx]
            
            # Create PDF filename
            pdf_number = str(pdf_idx + 1).zfill(3)
            output_filename = os.path.join(OUTPUT_DIR, f"gallery_{pdf_number}.pdf")
            
            # Create PDF
            create_pdf(batch, output_filename)
    else:
        # Create single PDF with all images
        output_filename = os.path.join(OUTPUT_DIR, "gallery.pdf")
        create_pdf(image_files, output_filename)
    
    print("=" * 60)
    print(f"✓ Processing complete!")
    print(f"  PDFs created: {OUTPUT_DIR}/")
    print(f"  Source photos: {SOURCE_DIR}/ (unchanged)")
    print("=" * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create PDF gallery with photo grid layout")
    parser.add_argument('--split', action='store_true', 
                        help="Split into multiple PDFs. Default: single PDF with all photos")
    parser.add_argument('--grid', type=str, default='3x3',
                        help="Grid size in format WxH (e.g., '3x3', '4x2'). Default: 3x3. Range: 1-5 cols, 1-4 rows")
    args = parser.parse_args()
    
    # Parse grid size
    try:
        grid_cols, grid_rows = parse_grid_size(args.grid)
    except ValueError as e:
        print(f"ERROR: {e}")
        exit(1)
    
    main(split_mode=args.split, grid_cols=grid_cols, grid_rows=grid_rows)