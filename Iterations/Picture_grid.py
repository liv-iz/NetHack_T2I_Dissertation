import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Step 1: Get all image paths
# Step 1: Get all image paths
image_paths = []
for root, dirs, files in os.walk("."):
    print(f"Looking in directory: {root}")
    for file in files:
        if "Acid_blob" in file and file.endswith((".png")):  # Add or remove file types as needed
            image_paths.append(os.path.join(root, file))
            print(f"Found image: {file}")


# Step 2: Read all images
images = [mpimg.imread(image_path) for image_path in image_paths]

# Check if there are images
if images:
    # Step 3: Create grid and display images
    fig, axs = plt.subplots(10, 1)  # 8x8 grid

    for img, ax in zip(images, axs.flatten()):
        ax.imshow(img)
        ax.axis('off')  # Hide axes
        ax.set_aspect('equal')  # Keep aspect ratio

    plt.show()
else:
    print("No images found.")