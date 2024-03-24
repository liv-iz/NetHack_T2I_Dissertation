import pandas as pd
import os
# Create DF with one tilename column (from nethack_tileset/Data_Gathering/Web Scraping Script and CSV/tileset_vanilla_titles.csv)
# and one GPT-4 description column (from nethack_tileset/Data_Gathering/GPT/GPT Descriptions/GPT Second Run CSV/tileset_gpt4_default.csv)
# and one style specification string

tile_name_path = 'nethack_tileset/Data_Gathering/Web Scraping Script and CSV/tileset_vanilla_titles.csv'
gpt4_description_path = 'nethack_tileset/Data_Gathering/GPT/GPT Descriptions/GPT Second Run CSV'

# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(gpt4_description_path) if f.endswith('.csv')]

# Initialize an empty DataFrame to hold all columns
all_columns_df = pd.DataFrame()

# Loop through each CSV file
for csv_file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(gpt4_description_path, csv_file))

    # Add each column to the new DataFrame
    for column in df.columns:
        all_columns_df[column] = df[column]


tile_name = pd.read_csv(tile_name_path)

prompts = pd.concat([tile_name, all_columns_df], axis=1)

prompts.to_csv('nethack_tileset/Data_Gathering/Data preparation/all_prompts_second_run.csv', index=False)

