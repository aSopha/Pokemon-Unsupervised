import requests
import pandas as pd
import time
from tqdm import tqdm

# How many Pokémon to get (Gen 1 is 1-151)
NUM_POKEMON = 386

# Store data
pokemon_list = []
all_moves = set()

# Get Pokémon data
for i in tqdm(range(1, NUM_POKEMON + 1)):
    url = f"https://pokeapi.co/api/v2/pokemon/{i}"
    response = requests.get(url)
    data = response.json()

    name = data['name']
    moves = [move['move']['name'] for move in data['moves']]

    pokemon_list.append({'name': name, 'moves': moves})

    # Collect all possible moves
    all_moves.update(moves)

    time.sleep(0.5)  # Be nice to the API

# Convert to sorted list of moves
all_moves = sorted(list(all_moves))

# Build binary matrix
rows = []
for pokemon in pokemon_list:
    row = {'name': pokemon['name']}
    for move in all_moves:
        row[move] = 1 if move in pokemon['moves'] else 0
    rows.append(row)

# Final DataFrame
df = pd.DataFrame(rows)

# Preview
print(df.head())

# Save to CSV
df.to_csv('pokemon_move_matrix.csv', index=False)
print(f"Saved {df.shape[0]} Pokémon with {df.shape[1]-1} moves to pokemon_move_matrix.csv")
