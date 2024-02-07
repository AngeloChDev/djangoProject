from .models import Teams, Players, Profiles,Games, Gols_Scored
from django.utils import timezone
from .utils import maketot_dict

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
      def upload_new_player(cls,new_player):#, old_team=None):
            try:
                  
                  if cls.search(Players, {'player':new_player['player']}):
                        raise djError('Plyer name exist')
                  if not cls.search(Teams,{'name':new_player['team']["name"]}):
                        raise djError('The team where you want to add the new player doesn t exist')
                  team=Teams.objects.get(name=new_player['team']["name"])
                  player = Players.objects.create(player=new_player['player'],team=team)
                  
                  old=dict()
                  if "profile" in new_player.keys():
                        cls.add_profile_toplayer(player,new_player["profile"])
                  if "old_team" in new_player.keys():
                        old = maketot_dict(new_player["old_team"])
                  old[now.year]=team.name
                  player.old_teams=old.copy()
                  player.save()
                  return True
            except djError as e:
                  print(e)
                  return None
      
      @staticmethod
      def add_profile_toplayer(player, profile):
            #player=Players.objects.get(id=player_id)
            print(player.player,bool(player.profile is None))
            if player.profile is None:
                  if isinstance(profile, dict):
                        obj_profile=Profiles.objects.create(**profile)
                        player.profile=obj_profile
                        obj_profile.save()
                  elif isinstance(profile,Profiles):
                        player.profile=profile
            else:
                  p=Profiles.objects.get(pk=player.profile.id)
                  Profiles.objects.select_for_update().filter(pk=player.profile.id).update(**profile)
                  p.refresh_from_db()
                  
            player.save()
            return True
            

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
      def get_it(model, kwargs):
            obj = model.objects.get(**kwargs)
            return obj

      @staticmethod
      def search(model, kwargs):
            return bool(model.objects.filter(**kwargs))



