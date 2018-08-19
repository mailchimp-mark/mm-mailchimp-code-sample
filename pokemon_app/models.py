# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Pokemon(models.Model):
    pokemon_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=255, null=True)

    def get_like_count(self):
        return Like.objects.filter(pokemon=self).count()

class Like(models.Model):
    pokemon = models.ForeignKey(Pokemon)