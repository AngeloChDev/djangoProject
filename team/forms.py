from profile import Profile
from typing import Any
from django import forms
from django.forms.fields import CharField,MultiValueField
from django.forms.widgets import  TextInput,MultiWidget,NumberInput, Widget,ChoiceWidget
from .models import Teams, Profiles, Players, Games, Gols_Scored
from .registration import Registrator, djError

class ADMlogin(forms.Form):
      text_input = forms.CharField(max_length=3)
      password_input = forms.CharField(min_length=8, widget=forms.PasswordInput)


class TeamsModelForm(forms.ModelForm):
      class Meta:
            model = Teams
            fields = "__all__"
            widgets={
                  
                  "name":forms.TextInput(attrs={"class":"form-control shadow fs-3 widht-4 m-auto"}),
                  "town":forms.TextInput(attrs={"class":"form-control shadow fs-3 widht-4 m-auto"}),
                  "color":forms.TextInput(attrs={"class":"form-control shadow fs-3 widht-4 m-auto","is_required":False}),
            
            }

class ProfileMultiValueField(forms.MultiValueField):
      def __init__(self, *args, **kwargs):
            
            fields = [
                  forms.CharField(),
                  forms.CharField(),
                  forms.CharField(),
            ]
            super(ProfileMultiValueField, self).__init__(fields, *args, **kwargs)
      
      def compress(self, values):
            print('gffgfgf',values)
            profile = Profiles.objects.create(height=float(values[0]), weight=float(values[1]), nationality=values[2])
            profile.save()
            return profile

class ProfileMultiWidget(forms.MultiWidget):
      def __init__(self, attrs=None):
            #attrs =  {"class":"form-control shadow mt-3 mb-4 fs-3"}
            self.widgets = [
                  NumberInput(attrs= {"placeholder":"height","class":"form-control p-2 m-auto m-2 shadow fs-3 widht-6 lil-widget-form"}),
                  NumberInput(attrs={"placeholder":"weight","class":"form-control shadow m-auto mt-3 mb-4 fs-3 widht-6 lil-widget-form"}),
                  TextInput(attrs={"placeholder":"nazionality","class":"form-control shadow m-auto mt-3 mb-4 fs-3 widht-6 lil-widget-form"}),
            ]
            super(ProfileMultiWidget, self).__init__(self.widgets, attrs)

      def decompress(self, value):
            if value:
                  return [value[0], value[1], value[2]]
            return ['', '', '']
      
      def format_output(self, rendered_widgets):
            return '<br>'.join(rendered_widgets)
      
class PlayersModelForm(forms.ModelForm):
      class Meta:
            model = Players
            fields = ['player', 'team', 'profile', 'old_teams']
            widgets={
                  
                  "player":forms.TextInput(attrs={"class":"form-control mt-2 mb-1 shadow fs-3 m-auto widht-6 lil-widget-form"}),
                  "team":forms.Select(attrs={"class":"fs-3"}),
                  "old_teams":forms.TextInput(attrs={"placeholder":"Year TeamName,..","class":"form-control shadow fs-3 m-auto widht-6 lil-widget-form","is_required":False}),
             
            }     


      def __init__(self, *args, **kwargs):
            super(PlayersModelForm, self).__init__(*args, **kwargs)
            self.fields['profile']=ProfileMultiValueField()
            self.fields['profile'].widget = ProfileMultiWidget()

      def is_valid(self) -> bool:
            if Registrator.search(Players,{'player':self.data['player']}):
                  raise ValueError('name value error')
            
            va_p={'height':float(self.data['profile_0']) , 'weight': float(self.data['profile_1']), 'nationality': self.data['profile_2']}
            #p=self.fields['profile'].compress(list(va_p.values()))

            new_player_profile_data={'player':self.data['player'],'team':{'name':Teams.objects.get(pk=int(self.data['team'])).name},'profile':va_p,'old_team':self.data['old_teams']}
            if Registrator.upload_new_player(new_player_profile_data):
                  print('oooook')
                  p=Players.objects.get(id=57)
                  va_p['height']+=2
                  Registrator.add_profile_toplayer(p,va_p)
                  return True
            









      #@classmethod
      #def confirm_values(cls,widget_player,widget_team,widget_profile,widget_old_teams):
      #      pass
      
      
      #      keys_profile=["height", "weight", "nationality"]
      #      widget_player = "ofotttozufffggg"#self.Meta.widgets["player"]["value"]
      #      widget_team = "HSV"#self.Meta.widgets["team"]["value"]
      #      widget_profile = "1.8 , 77, Italia"#self.Meta.widgets["profle"]["value"].split(',')
      #      widget_old_teams = "2023 HSV, 2022 Napoli"#self.Meta.widgets["old_teams"]["value"].split(',')
#
      #      profile_dict=dict()
      #      if widget_profile:
      #            profile_data=widget_profile.split(',')
      #            for k,v in zip(keys_profile,profile_data):
      #                  x=v.strip()
      #                  try:
      #                        profile_dict[k] = float(x)
      #                  except:
      #                        profile_dict[k] = v
      #      old_teams_dict=dict()
      #      if widget_old_teams:
      #            old_teams_list = widget_old_teams.split(',')
      #            data=[x.split() for x in old_teams_list]
      #            for j in data:
      #                  old_teams_dict[j[0]] = j[1]
#
      #      new_player={'player':widget_player, 'team':{"name":widget_team}, 'profile':profile_dict,"old_team":old_teams_dict }
      #      print(new_player)
      #      Registrator.upload_new_player(new_player)
      #      #player = Players.objects.create(**new_player)
      #      #player.save()
      #      return True

