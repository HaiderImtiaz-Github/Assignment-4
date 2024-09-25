from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

def browse_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if file_path:
        return file_path
    else:
        return None

def add_watermark(image_path, watermark_text="Haider Imtiaz"):
    # Open the original image
    image = Image.open(image_path).convert("RGBA")
    
    # Make the image editable
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))  # Transparent layer for the text
    drawing = ImageDraw.Draw(txt_layer)
    
    # Define the font and size (adjust font and size as needed)
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # Custom font size and font family
    except IOError:
        font = ImageFont.load_default()

    # Get image dimensions
    width, height = image.size
    
    # Calculate the bounding box of the watermark text using font.getbbox()
    text_bbox = drawing.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position for the watermark (bottom-right corner)
    x = width - text_width - 20  # 20px margin from the right
    y = height - text_height - 20  # 20px margin from the bottom
    
    # Add watermark to the transparent layer
    drawing.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 150))  # White text with some transparency

    # Combine the original image with the watermark layer
    watermarked_image = Image.alpha_composite(image, txt_layer)

    # Save the result (in PNG to retain transparency)
    watermarked_image_path = "watermarked_image_with_text.png"
    watermarked_image.convert("RGB").save(watermarked_image_path, "PNG")
    
    print(f"Watermark added. Image saved as {watermarked_image_path}")

    # Display the image (optional)
    watermarked_image.show()

def upload_and_watermark():
    image_path = browse_image()
    if image_path:
        watermark_text = "Haider Imtiaz"  # Watermark text
        add_watermark(image_path, watermark_text)

window = Tk()
window.title("Image Watermark")
window.minsize(400, 50)

window.columnconfigure(0, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(2, weight=1)

# Button to upload an image and add watermark
upload_button = Button(window, text="Upload Image and Add Watermark", command=upload_and_watermark)
upload_button.grid(column=1, row=1)

window.mainloop()
