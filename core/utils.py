import uuid
from PIL import Image, ImageDraw
import svgwrite
import os

# Function to create a unique SVG file for the box layout
def create_svg(length, breadth, height):
    """
    Generates an SVG file with the layout of the box based on the given dimensions.
    The SVG file is saved with a unique name to prevent overwriting.
    """
    svg_filename = f"box_layout_{uuid.uuid4()}.svg"
    dwg = svgwrite.Drawing(svg_filename, profile="tiny")
    # Add box design (panels)
    dwg.add(dwg.rect(insert=(0, 0), size=(length * 10, breadth * 10), fill="none", stroke="black"))
    dwg.add(dwg.text(f"Length: {length}", insert=(10, 20), fill="black"))
    dwg.add(dwg.text(f"Breadth: {breadth}", insert=(10, 40), fill="black"))
    dwg.add(dwg.text(f"Height: {height}", insert=(10, 60), fill="black"))
    dwg.save()
    print(f"SVG file saved as {svg_filename}")
    return svg_filename

# Function to generate a basic PSD layout
def generate_psd(length, breadth, height):
    """
    Creates a PSD file for the box layout with the given dimensions.
    The PSD file is saved with a unique name to prevent overwriting.
    """
    psd_filename = f"box_layout_{uuid.uuid4()}.psd"
    img = Image.new("RGB", (length * 10, breadth * 10), color="white")
    draw = ImageDraw.Draw(img)
    # Draw the layout
    draw.rectangle([10, 10, length * 10 - 10, breadth * 10 - 10], outline="black", width=3)
    draw.text((20, 20), f"Length: {length}", fill="black")
    draw.text((20, 40), f"Breadth: {breadth}", fill="black")
    draw.text((20, 60), f"Height: {height}", fill="black")
    img.save(psd_filename)
    print(f"PSD file saved as {psd_filename}")
    return psd_filename

# Placeholder function for converting SVG to CDR
def convert_svg_to_cdr(svg_filename, cdr_filename):
    """
    Placeholder function to convert SVG to CDR format.
    Ideally, you would use CorelDRAW's API or a compatible tool for this.
    This dummy function returns the file path for the CDR file.
    """
    dummy_cdr_path = cdr_filename
    print(f"Converting {svg_filename} to {dummy_cdr_path} (dummy implementation)")
    return dummy_cdr_path

# Function to clean up generated files (optional)
def cleanup_files(files):
    """
    Deletes the generated files from the file system.
    Useful for cleaning up after serving the files.
    """
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted file: {file}")
