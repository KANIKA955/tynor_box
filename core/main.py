from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import svgwrite

app = FastAPI()

class BoxLayoutRequest(BaseModel):
    width: int  # Width of the main panel (front/back)
    height: int  # Height of the box
    depth: int  # Depth of the side panels


def create_svg(width, height, depth):
    try:
        # File name
        svg_filename = "box_layout_corrected.svg"
        dwg = svgwrite.Drawing(svg_filename, profile="tiny", size=("1500px", "1500px"))

        # Colors and style
        border_color = "black"
        fill_color = "none"
        text_color = "blue"
        font_size = "12px"

        # Scale for visualization
        scale = 10

        # Scaled dimensions
        scaled_width = width * scale
        scaled_height = height * scale
        scaled_depth = depth * scale

        # Layout components (no gaps between sections)
        # Top Flap
        dwg.add(dwg.rect(insert=(scaled_depth, 0), size=(scaled_width, scaled_depth),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Top Flap", insert=(scaled_depth + 10, scaled_depth / 2), fill=text_color, font_size=font_size))

        # Front Panel
        dwg.add(dwg.rect(insert=(scaled_depth, scaled_depth), size=(scaled_width, scaled_height),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Front Panel", insert=(scaled_depth + 10, scaled_depth + 20), fill=text_color, font_size=font_size))

        # Back Panel (directly below the Front Panel)
        dwg.add(dwg.rect(insert=(scaled_depth, scaled_depth + scaled_height), size=(scaled_width, scaled_height),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Back Panel", insert=(scaled_depth + 10, scaled_depth + scaled_height + 20),
                         fill=text_color, font_size=font_size))

        # Bottom Flap (directly below the Back Panel)
        dwg.add(dwg.rect(insert=(scaled_depth, scaled_depth + scaled_height * 2), size=(scaled_width, scaled_depth),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Bottom Flap", insert=(scaled_depth + 10, scaled_depth + scaled_height * 2 + 20),
                         fill=text_color, font_size=font_size))

        # Left Side Panel (aligned to the left of the Front Panel)
        dwg.add(dwg.rect(insert=(0, scaled_depth), size=(scaled_depth, scaled_height),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Left Side Panel", insert=(10, scaled_depth + 20), fill=text_color, font_size=font_size))

        # Right Side Panel (aligned to the right of the Front Panel)
        dwg.add(dwg.rect(insert=(scaled_depth + scaled_width, scaled_depth), size=(scaled_depth, scaled_height),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Right Side Panel", insert=(scaled_depth + scaled_width + 10, scaled_depth + 20),
                         fill=text_color, font_size=font_size))

        # Left Glue Flap (aligned to the left of the Left Side Panel)
        dwg.add(dwg.rect(insert=(-scaled_depth, scaled_depth), size=(scaled_depth, scaled_height),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Left Glue Flap", insert=(-scaled_depth + 10, scaled_depth + 20),
                         fill=text_color, font_size=font_size))

        # Right Glue Flap (aligned to the right of the Right Side Panel)
        dwg.add(dwg.rect(insert=(scaled_depth + scaled_width + scaled_depth, scaled_depth), size=(scaled_depth, scaled_height),
                         stroke=border_color, fill=fill_color))
        dwg.add(dwg.text("Right Glue Flap", insert=(scaled_depth + scaled_width + scaled_depth + 10, scaled_depth + 20),
                         fill=text_color, font_size=font_size))

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
