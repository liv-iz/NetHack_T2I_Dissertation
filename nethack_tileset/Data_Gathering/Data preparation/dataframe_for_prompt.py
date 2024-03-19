import pandas as pd
import os
# Create DF with one tilename column (from nethack_tileset/Data_Gathering/Web Scraping Script and CSV/tileset_vanilla_titles.csv)
# and one GPT-4 description column (from nethack_tileset/Data_Gathering/GPT/GPT Descriptions/GPT Second Run CSV/tileset_gpt4_default.csv)
# and one style specification string

tile_name_path = 'nethack_tileset/Data_Gathering/Web Scraping Script and CSV/tileset_vanilla_titles.csv'
gpt4_description_path = 'nethack_tileset/Data_Gathering/GPT/GPT Descriptions/GPT Second Run CSV'

# Get path for each csv file in gpt4_description_path
gpt4_description_files = [f for f in os.listdir(gpt4_description_path) if f.endswith('.csv')]

tile_name = pd.read_csv(tile_name_path)

# Dictionary to store dataframes
gpt_description = {}

# Read each file into a dataframe
for file in gpt4_description_files:
    # Remove the .csv extension from the file name
    df_name = os.path.splitext(file)[0]
    # Read the file into a dataframe and store it in the dictionary
    gpt_description[df_name] = pd.read_csv(os.path.join(gpt4_description_path, file))

print(gpt_description.keys())

# List of new names
new_names = ["default", "default_short", "stability", "technical"]

# Dictionary to store renamed dataframes
renamed_gpt_description = {}

# Rename each dataframe
for new_name, (old_name, df) in zip(new_names, gpt_description.items()):
    # Store the dataframe in the new dictionary with the new name
    renamed_gpt_description[new_name] = df

# Replace the old dictionary with the new one
gpt_description = renamed_gpt_description

# Rename columns in each dataframe
for df_name, df in gpt_description.items():

    # Rename columns
    df.columns = [f"{df_name}"]

# Concatenate all dataframes along the column axis
combined_df = pd.concat(gpt_description.values(), axis=1)

# Add the combined dataframe to the tile_name dataframe
tile_name = pd.concat([tile_name, combined_df], axis=1)

tile_name