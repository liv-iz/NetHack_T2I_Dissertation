from PIL import Image
import os
# Directory containing images
root_dir = os.path.dirname(os.path.abspath(__file__))

# List to store images
images = []

# Loop through all subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "grid.png":
            # Open the image file
            img = Image.open(os.path.join(dirpath, filename))
            img.show()  # Show the image
