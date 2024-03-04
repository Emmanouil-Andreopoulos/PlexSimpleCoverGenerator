import os
# Import Pillow
from PIL import Image, ImageDraw, ImageFont


def draw_multiline_text(draw, text, font, position, max_width, max_height, line_spacing):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    line_height = draw.textbbox((0, 0), lines[0], font=font)[3] - draw.textbbox((0, 0), lines[0], font=font)[1]

    total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing  # Add spacing between lines

    for i, line in enumerate(lines):
        line_bbox = draw.textbbox((0, 0), line, font=font)

        x = position[0] + (max_width - line_bbox[2] + line_bbox[0]) // 2  # Center horizontally
        y = position[1] + (max_height - total_height) // 2 + i * (
                line_height + line_spacing)  # Center vertically with spacing

        draw.text((x, y), line, font=font, fill="white")


def generate_image(folder_path):
    # Define line spacing
    line_spacing = 10
    # Define image dimensions
    width, height = 800, 1200

    # Choose a font size (adjust as needed)
    font_size = 60

    # Create a new image with a darker blue background
    image = Image.new("RGB", (width, height), "#004080")  # Hex color code for a darker blue

    # Get a drawing context on the image
    draw = ImageDraw.Draw(image)

    # Use a larger font to cover the whole width
    font = ImageFont.truetype("arial.ttf",
                              font_size)  # You may need to provide the path to a TTF font file on your system

    # Calculate the maximum width and height for the text
    max_text_width = width * 0.9  # Adjust as needed
    max_text_height = height * 0.9  # Adjust as needed

    # Calculate the text position to center it
    x = (width - max_text_width) // 2
    y = (height - max_text_height) // 2

    # Draw multiline text on the image in white color with spacing
    draw_multiline_text(draw, os.path.basename(folder_path), font, (x, y), max_text_width, max_text_height,
                        line_spacing)

    # Save the image to the specified path
    output_path = os.path.join(folder_path, f"show.png")
    image.save(output_path)
    return f"Image generated and saved at {output_path}"
