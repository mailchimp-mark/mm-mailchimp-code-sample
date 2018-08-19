from django.test import TestCase

from pokemon_app.models import Pokemon


class PokemonBaseTestCase(TestCase):
    def setUp(self):
        self.test_data = [
            {
                'pokemon_id': '27',
                'name': 'Sandshrew',
                'image_url': 'https://pictures.com/Sandshrew',
                'bio': 'Awesome pokemon',
            },
            {
                'pokemon_id': '35',
                'name': 'Clefairy',
                'image_url': 'https://pictures.com/Clefairy',
                'bio': 'Great pokemon',
            },
            {
                'pokemon_id': '38',
                'name': 'Ninetales',
                'image_url': 'https://pictures.com/Ninetales',
                'bio': 'Nine tailed pokemon',
            },
        ]

    def create_pokemons(self):
        """Create Pokemons for tests"""
        for item in self.test_data:
            Pokemon.objects.create(
                pokemon_id=item['pokemon_id'],
                name=item['name'],
                image_url=item['image_url'],
                bio=item['bio'],
            )