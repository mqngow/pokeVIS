from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

POKEAPI_URL = "https://pokeapi.co/api/v2"

# Get Pokemon from PokeAPI
def get_pokemon(identifier):
    try:
        identifier = str(identifier).lower().strip()
        response = requests.get(f"{POKEAPI_URL}/pokemon/{identifier}", timeout=10)

        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        data = response.json()

        # Get Pokemon abilities
        abilities = [{
            'name': a['ability']['name'],
            'is_hidden': a['is_hidden']
        } for a in data['abilities']]

        # Get level-up moves (moves not including tms etc)
        moves = []
        for move in data['moves'][:50]: # Set a limit to display only the first 50 moves
            move_name = move['move']['name']
            move_url = move['move']['url']
            level_learned = None
            for version_detail in move['version_group_details']:
                if version_detail['move_learn_method']['name'] == 'level-up':
                    level_learned = version_detail['level_learned_at']
                    break

            if level_learned is not None:
                # Get move time
                try:
                    move_response = requests.get(move_url, timeout=5)
                    move_data = move_response.json()
                    move_type = move_data['type']['name']
                except:
                    move_type = 'normal'

                move.append({
                    'name': move_name,
                    'level': level_learned,
                    'type': move_type
                })

        # Sort by level
        moves.sort(key=lambda x: x['level'])

        # Format
        pokemon = {
            'id': data['id'],
            'name': data['name'].title(),
            'sprite': data['sprites']['front_default'],
            'height': data['height'] / 10, # To meters
            'weight': data['weight'] / 10, # To kilograms
            'types': [t['type']['name'] for t in data['types']],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'abilities': abilities,
            'moves': moves
        }

        return pokemon
    
    except requests.RequestException as e:
        print(f"Error fetching Pokemon: {e}")
        return None
    
# Get ability
def get_ability(ability_name):
    try:
        ability_name = str(ability_name).lower().strip()
        response = requests.get(f"{POKEAPI_URL}/ability/{ability_name}", timeout=10)
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        data = response.json()
        
        # Get Pokemon that have the ability
        pokemon_with_ability = []
        for pokemon in data['pokemon'][:25]:  # Set limit to 25 pokemon
            pokemon_with_ability.append({
                'name': pokemon['pokemon']['name'],
                'is_hidden': pokemon['is_hidden']
            })
        
        # Get effect description
        effect = 'No description available'
        for entry in data['effect_entries']:
            if entry['language']['name'] == 'en':
                effect = entry['effect']
                break
        
        # Get short effect if possible
        short_effect = effect
        for entry in data['effect_entries']:
            if entry['language']['name'] == 'en' and 'short_effect' in entry:
                short_effect = entry['short_effect']
                break
        
        # Format
        ability = {
            'name': data['name'].replace('-', ' ').title(),
            'id': data['id'],
            'effect': effect,
            'short_effect': short_effect,
            'pokemon': pokemon_with_ability
        }
        
        return ability
    
    except requests.RequestException as e:
        print(f"Error fetching ability: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)