# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

from pokemon_app.models import Pokemon, Like

def index(request):
    """Main list page"""
    context = {}

    #Create session key, value if doesn't exist
    if not request.session.get('liked_user_ids', None):
        request.session['liked_user_ids'] = []

    context['pokemons'] = Pokemon.objects.all()
    return render(request, 'pokemon_app/pokemon_list.html', context)

def create_like(request):
    """AJAX endpoint for creating Likes"""
    pokemon_id = request.POST.get('pokemon-like-id', None)
    context = {}

    if not request.session.get('liked_user_ids', None):
        request.session['liked_user_ids'] = []

    if pokemon_id not in request.session.get('liked_user_ids'):
        Like.objects.create(pokemon_id=pokemon_id)
        context['liked'] = True
        request.session['liked_user_ids'].append(pokemon_id)
        request.session.modified = True

    context['pokemon_likes'] = Pokemon.objects.get(pk=pokemon_id).get_like_count()

    return JsonResponse(context, status=200)