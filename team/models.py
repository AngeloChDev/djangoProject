from enum import unique
from django.db import models

# Create your models here.

class Teams(models.Model):
      name=  models.CharField(unique=True, max_length=50,blank=False)
      town = models.CharField(max_length=50,blank=False)
      color = models.CharField(max_length=50,blank=False,null=True)
      #games= models.OneToOneField(Games,on_delete=models.CASCADE, verbose_name="games" )
      
class Profiles(models.Model):
      height = models.FloatField(blank=False)
      weight = models.FloatField(blank=False)
      nationality = models.CharField(max_length=50,blank=False)


class Players(models.Model):
      player=models.CharField(unique=True, max_length=50,blank=False)
      team= models.ForeignKey(Teams,on_delete=models.CASCADE, verbose_name="teams" )
      profile = models.ForeignKey(Profiles,null=True, on_delete=models.CASCADE,verbose_name="profiles" )
      old_teams = models.JSONField(null=True,verbose_name="old teams")
#,

class Games(models.Model):
      team= models.ForeignKey(Teams,on_delete=models.CASCADE, verbose_name="teams" )
      game_date = models.DateField()
      opponent=models.CharField(max_length=50,blank=False)
      score = models.CharField(max_length=20,null=True)

class Gols_Scored(models.Model):
      game = models.ForeignKey(Games, on_delete=models.CASCADE, verbose_name="games" )
      minute = models.FloatField()
      player = models.ForeignKey(Players, on_delete=models.CASCADE, verbose_name="players" )





#default=dict