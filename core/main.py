from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import svgwrite
from PIL import Image
import os
import subprocess

app = FastAPI()

class BoxLayoutRequest(BaseModel):
    length: int
    breadth: int
    height: int
    format: str = "svg"

def create_svg(length, breadth, height):
    svg_filename = "tynor_box_layout.svg"
    dwg = svgwrite.Drawing(svg_filename, profile="tiny")

    scale = 10  
    border_color = "black"
    fill_color = "white"

    # Front and back
    dwg.add(dwg.rect(insert=(scale, scale), size=(length * scale, height * scale), fill=fill_color, stroke=border_color))
    dwg.add(dwg.rect(insert=((length + breadth + 2) * scale, scale), size=(length * scale, height * scale), fill=fill_color, stroke=border_color))

    # Left and right sides
    dwg.add(dwg.rect(insert=(scale, (height + 2) * scale), size=(breadth * scale, height * scale), fill=fill_color, stroke=border_color))
    dwg.add(dwg.rect(insert=((length + breadth + 2) * scale, (height + 2) * scale), size=(breadth * scale, height * scale), fill=fill_color, stroke=border_color))

    # Top and bottom
    dwg.add(dwg.rect(insert=(scale, (height + breadth + 4) * scale), size=(length * scale, breadth * scale), fill=fill_color, stroke=border_color))
    dwg.add(dwg.rect(insert=((length + breadth + 2) * scale, (height + breadth + 4) * scale), size=(length * scale, breadth * scale), fill=fill_color, stroke=border_color))

    dwg.save()
    return svg_filename

def convert_svg_to_psd(svg_filename):
    psd_filename = "tynor_box_layout.psd"
    png_filename = "temp.png"

    try:
        # Convert SVG to PNG
        subprocess.run(["cairosvg", svg_filename, "-o", png_filename], check=True)

        # Convert PNG to PSD
        img = Image.open(png_filename)
        img.save(psd_filename, "PSD")
    finally:
        # Clean up temporary PNG file
        if os.path.exists(png_filename):
            os.remove(png_filename)

    return psd_filename

def convert_psd_to_cdr(psd_filename):
    cdr_filename = "tynor_box_layout.cdr"

    # CorelDRAW Automation Placeholder
    try:
        subprocess.run(["path/to/coreldraw", psd_filename, "/convert", cdr_filename], check=True)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CorelDRAW not found or conversion failed.")

    return cdr_filename

@app.post("/generate-box-layout/")
def generate_box_layout(request: BoxLayoutRequest):
    length = request.length
    breadth = request.breadth
    height = request.height
    format = request.format

    if format == "svg":
        svg_file = create_svg(length, breadth, height)
        return FileResponse(svg_file, media_type="image/svg+xml", filename=svg_file)
    elif format == "psd":
        svg_file = create_svg(length, breadth, height)
        psd_file = convert_svg_to_psd(svg_file)
        return FileResponse(psd_file, media_type="application/octet-stream", filename=psd_file)
    elif format == "cdr":
        svg_file = create_svg(length, breadth, height)
        psd_file = convert_svg_to_psd(svg_file)
        cdr_file = convert_psd_to_cdr(psd_file)
        return FileResponse(cdr_file, media_type="application/x-cdr", filename=cdr_file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Please choose 'svg', 'psd', or 'cdr'.")
