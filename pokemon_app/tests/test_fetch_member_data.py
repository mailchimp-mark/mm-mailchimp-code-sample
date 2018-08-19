# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from pokemon_app.cron import fetch_pokemon_data
from pokemon_app.models import Pokemon

from pokemon_app.tests import PokemonBaseTestCase

import mock, json


class PokemonInitialCallTestCase(PokemonBaseTestCase):
    @mock.patch('requests.get')
    def test_pokemons_get_created(self, request_mock):
        """Pokemons should get created when calling fetch_pokemon_data on empty DB
        and non-empty response from API"""
        expected_count = 3
        request_mock.return_value = mock.Mock(content=json.dumps(self.test_data))
        fetch_pokemon_data()

        assert Pokemon.objects.all().count() == expected_count

    @mock.patch('requests.get')
    def test_empty_response_from_api(self, request_mock):
        """No Pokemons should get created if API response is empty"""
        expected_count = 0
        request_mock.return_value = mock.Mock(content=json.dumps({}))
        fetch_pokemon_data()

        assert Pokemon.objects.all().count() == expected_count


class PokemonUpdateTestCase(PokemonBaseTestCase):
    def setUp(self):
        super(PokemonUpdateTestCase, self).setUp()
        self.create_pokemons() # creates 3 pokemon

    @mock.patch('requests.get')
    def test_new_pokemon_created_when_item_added_to_response(self, request_mock):
        """Adding item to API response should create an additional record in DB"""
        expected_count = 4
        self.test_data.append({
            'pokemon_id': '150',
            'name': 'Mewtwo',
            'image_url': 'https://pictures.com/mewtwo',
            'bio': 'Strongest pokemon ever',
        })

        request_mock.return_value = mock.Mock(content=json.dumps(self.test_data))
        fetch_pokemon_data()

        self.assertEqual(Pokemon.objects.all().count(), expected_count)

    @mock.patch('requests.get')
    def test_no_pokemons_created_if_data_hasnt_changed(self, request_mock):
        """When there are no updates to API response, no new DB records should be created"""
        expected_count = 3
        request_mock.return_value = mock.Mock(content=json.dumps(self.test_data))
        fetch_pokemon_data()

        self.assertEqual(Pokemon.objects.all().count(), expected_count)

    @mock.patch('requests.get')
    def test_field_update_for_updated_api_data(self, request_mock):
        """If there is an update to the bio and/or image_url of a pre-existing Pokemon, updated API
        fields should be updated in DB"""
        new_bio = 'Ninetails now only has eight tails'
        pokemon_item = self.test_data[-1]
        pokemon_item['bio'] = new_bio

        request_mock.return_value = mock.Mock(content=json.dumps(self.test_data))
        fetch_pokemon_data()

        pokemon = Pokemon.objects.filter(pokemon_id=pokemon_item['pokemon_id']).first()
        self.assertEqual(pokemon.bio, new_bio)

