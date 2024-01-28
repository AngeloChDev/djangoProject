from .models import Teams, Players, Profiles,Games, Gols_Scored
from django.utils import timezone

now=timezone.now()
class djError(Exception):
      def __init__(self, message) -> None:
            super().__init__(message)
            self.message = message
      def __str__(self):
            return f"{self.message}"


class Registrator:



      teams={'HSV':{'name':'HSV', 'town':'Hamburg(DE)', 'color':'Blue'}, 
            'St.Pauli' :{'name':'St.Pauli', 'town':'Hamburg(DE)', 'color':'Black'}, 
            'Napoli': {'name':'Napoli', 'town':'Napoli(IT)', 'color':'Light-Blue'}}

      profiles ={
            "name1":{'height':1.50, 'weight':70,'nationality':'Deutchland'},
            "name2":{'height':1.60, 'weight':80,'nationality':'Deutchland'},
            "name3":{'height':1.650, 'weight':75,'nationality':'Franch'},
            "name4":{'height':1.70, 'weight':85,'nationality':'Argentina'},
            "name5":{'height':1.650, 'weight':77,'nationality':'Italy'},
            "name6":{'height':1.74,'weight':82,'nationality':'Italy'},
                 
      }


      players = [
            {"player": "name1", "team": teams['HSV'],"profile":profiles["name1"]},
            {"player": "name2", "team": teams['HSV'],"profile":profiles["name2"]},
            {"player": "name3", "team": teams['St.Pauli'],"profile":profiles["name3"]},
            {"player": "name4", "team": teams['Napoli'], "profile":profiles["name4"]},
            {"player": "name5", "team": teams['Napoli'], "profile":profiles["name5"]},
            {"player": "name6", "team": teams['St.Pauli'],"profile":profiles["name6"]},
      ]

      
      games=[
            {'gameRegistration_data':'2023-06-12', 'opponent':'St.Pauli', 'score':2},
            {'game_data':'2023-06-18', 'opponent':'Napoli', 'score':6},
            {'game_data':'2023-06-24', 'opponent':'', 'score':3},
      ]


      @classmethod
      def upload_teams(cls, new_team):
            try:

                  if  cls.search(Teams, {'name': new_team['name']}):
                        raise djError('team already exist')
                  team=Teams.objects.create(**new_team)
                  team.save()
                  
            except djError as e :
                  print(e)
                  return None
            
      @classmethod
      def upload_new_player(cls,new_player, old_team=None):
            try:
                  if cls.search(Players, {'player':new_player['player']}):
                        raise djError('Plyer name exist')
                  if not cls.search(Teams,{'name':new_player['team']["name"]}):
                        raise djError('The team where you want to add the new player doesn t exist')
                  team=Teams.objects.get(name=new_player['team']['name'])
                  player = Players.objects.create(player=new_player['player'],team=team)
                  
                  if new_player["profile"] is not None:
                        player_profile=Profiles.objects.create(**new_player["profile"])
                        player.profile=player_profile
                        #player_profile=player.profiles_set.create(**new_player["profile"])
                        player_profile.save()
                  if old_team is not None:
                        for k,v in old_team.items():
                              player.old_teams[k]=v
                  
                  player.old_teams[now.year]=team.id
                  player.save()
            except djError as e:
                  print(e)
                  return None
      
      @staticmethod
      def add_profile_toplayer(player_id, profile):
            player=Players.objects.get(id=player_id)
            if not bool(player.profile):
                  player_profile=Profiles.objects.create(**profile)
                  player.profile=player_profile
                  player_profile.save()
            else:
                  Profiles.objects.filter(pk=player.profile.id).update(**profile)
            

      @staticmethod
      def delete_all_tb(tb, kwargs=None):
            if kwargs is not None:
                  return tb.objects.filter(**kwargs).delete()
            return tb.objects.all().delete()

      @classmethod
      def upload_defoult(cls):
            for i in cls.teams.values():
                  cls.upload_teams(i)
            
            for p in cls.players:
                  cls.upload_new_player(p)

      @staticmethod
      def search(model, kwargs):
            return bool(model.objects.filter(**kwargs))



