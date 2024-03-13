from PIL import Image
import os

# Grid size
rows = 2
cols = 5

# Directory containing images
dir_path = os.path.dirname(os.path.abspath(__file__))

# List to store images
images = []

# Loop through all files in the directory
for filename in os.listdir(dir_path):
    if filename.endswith(".png"):
        # Open the image file
        img = Image.open(os.path.join(dir_path, filename))
        # Append the image to the list
        images.append(img)

# Individual image size
img_width, img_height = images[0].size

# Total grid size
grid_width = cols * img_width
grid_height = rows * img_height

# Create a new image of the size of the grid
new_img = Image.new('RGB', (grid_width, grid_height))

# Loop through the images and paste them into the grid
for index, img in enumerate(images):
    row = index // cols
    col = index % cols
    new_img.paste(img, (col * img_width, row * img_height))

# Save the new image
new_img.save(os.path.join(dir_path)+'/grid.png')