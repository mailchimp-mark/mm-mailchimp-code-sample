# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse

from pokemon_app.models import Pokemon, Like
from pokemon_app.tests import PokemonBaseTestCase

import mock, json


class IndexViewTestCase(PokemonBaseTestCase):
    def setUp(self):
        super(IndexViewTestCase, self).setUp()
        self.create_pokemons()

    def test_index_view_returns_current_Pokemons(self):
        """index view should successfully render page with all Pokemons in db"""
        pokemons_qs = Pokemon.objects.all()
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            all(pokemon.name in response.content for pokemon in Pokemon.objects.all())
        )

    def test_session_creation(self):
        """index view should create a session store for anonymous users on their initial visit"""
        response = self.client.get(reverse('index'))
        self.assertEqual(self.client.session['liked_user_ids'], [])

    def test_index_view_should_render_likes_on_pokemons(self):
        """If a Pokemon has an associated like, our rendered page should reflect that"""
        pokemon = Pokemon.objects.all().first()
        Like.objects.create(pokemon=pokemon)
        response = self.client.get(reverse('index'))

        self.assertContains(response, "<span class='total-likes'>1</span>")

class CreateLikeViewTestCase(PokemonBaseTestCase):
    def setUp(self):
        super(CreateLikeViewTestCase, self).setUp()
        self.create_pokemons()

    def test_create_like(self):
        """Anonymous user should be able to create a Like for
        a Pokemon"""
        pokemon = Pokemon.objects.all().first()
        r = self.client.post(
            reverse('create_like'),
            {'pokemon-like-id': pokemon.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(Like.objects.all().count(), 1)

    def test_not_create_like_for_current_anon_already_liked(self):
        """Anonymous user should not be able to create multiple likes
        for any one Pokemon"""
        pokemon = Pokemon.objects.all().first()

        r = self.client.post(
            reverse('create_like'),
            {'pokemon-like-id': pokemon.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        r = self.client.post(
            reverse('create_like'),
            {'pokemon-like-id': pokemon.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(Like.objects.all().count(), 1)

