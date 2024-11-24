import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def month_to_abbreviation(month_name):
    # Create a dictionary mapping full month names to their 3-letter abbreviations
    month_dict = {
        "January": "Jan",
        "February": "Feb",
        "March": "Mar",
        "April": "Apr",
        "May": "May",
        "June": "Jun",
        "July": "Jul",
        "August": "Aug",
        "September": "Sep",
        "October": "Oct",
        "November": "Nov",
        "December": "Dec"
    }
    
    # Return the 3-letter abbreviation for the given month
    return month_dict.get(month_name, "Invalid month")

def draw_centered_text(image_path, text_list, font_path, font_size, positions, output_path, monthShort):
    """Draws multiple pieces of text centered at specified positions on an image.

    Args:
        image_path (str): Path to the input image.
        text_list (list of str): List of text strings to be drawn.
        font_path (str): Path to the .ttf font file.
        font_size (int): Font size for the text.
        positions (list of tuple): List of (x, y) tuples specifying positions for each text.
        output_path (str): Path to save the output image.
    """
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    for text, position in zip(text_list, positions):
        # Get the size of the text to be drawn using the modern method
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
        
        # Calculate the position to center the text at the specified location
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        
        # Draw the text on the image
        draw.text((x, y), text, font=font, fill="white")

    font = ImageFont.truetype(font_path, 100)

    # Get the size of the text to be drawn using the modern method
    text_width, text_height = draw.textbbox((0, 0), monthShort, font=font)[2:4]
        
    # Calculate the position to center the text at the specified location
    x = 800 - text_width // 2
    y = 200 - text_height // 2
        
    # Draw the text on the image
    draw.text((x, y), monthShort, font=font, fill="white")

    # Convert to RGB if the image is in RGBA mode (necessary for saving as JPEG)
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Save the modified image as JPEG
    image.save(output_path, "JPEG")

def main_create(first, second, third, month, year):

    monthShort = month_to_abbreviation(month) + " " + year

    image_path = "Graphics/Reds Rollover Post Draft.png"
    output_path = f"thumbnails/{month}-{year}-results.jpg"
    font_path = "Graphics/WorkSans-VariableFont_wght.ttf"  # Change this to the path of your .ttf font
    font_size = 50
    text_list = [first, second, third]
    positions = [(275, 560), (800, 560), (1350, 560)]  # Example positions for the text  

    

    draw_centered_text(image_path, text_list, font_path, font_size, positions, output_path, monthShort)

# Run the program
if __name__ == "__main__":
    main("First Place Winner", "Second Place Winner", "Third Place Winner","November", "2024")
