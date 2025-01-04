from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import svgwrite

app = FastAPI()

class BoxLayoutRequest(BaseModel):
    width: int  # Width of the box
    height: int  # Height of the box
    depth: int  

def create_svg(width, height, depth):
    try:
        # File name
        svg_filename = "box_layout.svg"
        dwg = svgwrite.Drawing(svg_filename, profile="tiny", size=("2000px", "2000px"))

        # Colors and style
        border_color = "black"
        text_color = "black"
        font_size = "15px"

        # Scale factor for visualization
        scale = 10

        # Scaled dimensions
        scaled_width = width * scale
        scaled_height = height * scale
        scaled_depth = depth * scale

        # Base offsets for placement
        x_offset = 100
        y_offset = 100

        # Adjusted panel placements based on the reference image
        panels = [
            # Panel number, position (x, y), size (width, height)
            ("1", (x_offset + scaled_depth, y_offset), (scaled_width, scaled_depth / 2)),  # Top flap above back
            ("2", (x_offset + scaled_depth, y_offset + scaled_depth / 2), (scaled_width, scaled_depth / 2)),  # Bottom flap above back
            ("3", (x_offset + scaled_depth, y_offset + scaled_depth), (scaled_width, scaled_height)),  # Back panel
            ("4", (x_offset + scaled_depth + scaled_width, y_offset), (scaled_depth / 2, scaled_depth / 2)),  # Top-left corner of 7 (half width of 7)
            ("5", (x_offset + scaled_depth + scaled_width, y_offset + scaled_depth), (scaled_depth / 2, scaled_height)),  # Right side panel
            ("6", (x_offset + scaled_depth + scaled_width, y_offset + scaled_depth + scaled_height), (scaled_depth / 2, scaled_depth / 2)),  # Right-bottom flap under 5
            ("7", (x_offset + scaled_depth + scaled_width + scaled_depth / 2, y_offset), (scaled_width, scaled_depth / 2)),  # Top flap above front
            ("8", (x_offset + scaled_depth + scaled_width + scaled_depth / 2, y_offset + scaled_depth), (scaled_width, scaled_height)),  # Front panel
            ("9", (x_offset + scaled_depth + scaled_width + scaled_depth / 2, y_offset + scaled_depth + scaled_height), (scaled_width, scaled_depth / 2)),  # Bottom flap under 8
            ("10", (x_offset + scaled_depth + scaled_width + scaled_width, y_offset), (scaled_depth / 2, scaled_depth / 2)),  # Top-right corner of 7 (half width of 7)
            ("11", (x_offset + scaled_depth + scaled_width + scaled_width + scaled_depth / 2, y_offset + scaled_depth / 2), (scaled_depth / 2, scaled_height)),  # Right strip
            ("12", (x_offset + scaled_depth + scaled_width + scaled_width + scaled_depth / 2, y_offset + scaled_depth / 2 + scaled_height), (scaled_depth / 2, scaled_depth / 2)),  # Right-bottom corner
        ]

        # Draw panels
        for panel_num, pos, size in panels:
            dwg.add(dwg.rect(insert=pos, size=size, stroke=border_color, fill="none"))
            dwg.add(dwg.text(panel_num, insert=(pos[0] + size[0] / 2, pos[1] + size[1] / 2),
                             fill=text_color, font_size=font_size, text_anchor="middle"))

        dwg.save()
        return svg_filename

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating SVG: {str(e)}")

@app.post("/generate-box-layout/")
def generate_box_layout(request: BoxLayoutRequest):
    try:
        svg_file = create_svg(request.width, request.height, request.depth)
        return FileResponse(svg_file, media_type="image/svg+xml", filename=svg_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
