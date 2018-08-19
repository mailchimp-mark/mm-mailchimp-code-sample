# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pokemon_app.models import Like, Pokemon
import json, requests

def fetch_pokemon_data():
    """Fetch response from pokemon api and synchronize data
    with our db"""
    r = requests.get('https://www.pokemonapi.com/v2/pokemon')
    pokemon_list = json.loads(r.content)
    for item in pokemon_list:
        # check to see if user exists
        obj, created = Pokemon.objects.get_or_create(
            pokemon_id=item['pokemon_id'],
            name=item['name'],
        )
        if created:
            obj.bio = item['bio']
            obj.image_url = item['image_url']
            obj.save()
        else:
            if obj.bio != item['bio']:
                obj.bio = item['bio']
                obj.save()

