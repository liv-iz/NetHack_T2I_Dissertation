import pandas as pd


# Set up our df for descriptions
tile_names = pd.read_csv("tileset_vanilla_titles.csv")
tile_descriptions = pd.read_csv("tileset_gpt_4_answers.csv")

tile_names = tile_names.join(tile_descriptions)
tile_names['prompt'] = tile_names["Title"] + ' from the game Nethack. ' + (tile_names["GPT-4 description"] + 'In the style of Pixel Art.')
tile_names['neg_prompt'] = '2D, shadows, dark, expansive, 8K, 4K'
tile_names[:10].to_csv("tileset_prompts_with_tile_name.csv", index=False)
