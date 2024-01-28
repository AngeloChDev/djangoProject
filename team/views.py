from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from team.registration import Registrator, djError
from .models import Teams, Players, Profiles,Games, Gols_Scored
from django.contrib.redirects.apps import RedirectsConfig
from time import time
from .game import PlayGame
from .forms import TeamsModefForm
import json
from .more_settings import MORE_HOME

class HomePageView(TemplateView):
      template_name = "home.html"
      #Registrator.upload_defoult()
      #Registrator.add_profile_toplayer(1,{'height':10, 'weight':70,'nationality':'Deutchland'})
      def get_context_data(self):
            context={"home":MORE_HOME}
            return context

class TeamsPageView(TemplateView):
      template_name="teams.html"

      def get_context_data(self):
            teams = Teams.objects.all()
            form= TeamsModefForm()
            context = {"teams": teams, "form":form}

            return context
      
class AllPlayersPageView(TemplateView):
      template_name = "all_players.html"

      def get_context_data(self):
            players = Players.objects.all()
            context = {"players": players}
            return context
    

class HomePlayerPageView(TemplateView):
      template_name = "info_player.html"

      def get_context_data(self,player_id):
            old=[]
            players = Players.objects.all()
            info_player = Players.objects.get(id=player_id)
            for k,v in info_player.old_teams.items():
                  team=Teams.objects.get(id=v)
                  old.append({'year':k,'team':team})
            context = {"players": players, "info_player":info_player,"old":old}
            return context
  
class GamePageView(TemplateView):
      template_name = "game.html"
      run_game = None
      start, end = 0, 0
      rounds = 0
      def get(self, request):
            if GamePageView.run_game is not None:
                  self.start=time()
                  return render(request,'play.html',GamePageView.run_game.context) 
            return render(request, self.template_name)
      
      def post(self, request):
            form = request.POST.get("submit_btn")
            if form=='start_game':
                  num1 = request.POST.get('player_home')
                  num2 = request.POST.get('player_ospit')
                  value = {'home':num1,'ospit':num2}
                  context = self.get_players(value)
                  context['quiz'] = GamePageView.run_game.make_quiz()
                  GamePageView.run_game.context = context
                  self.start=time()
                  return render(request,'play.html',context) #render(request, 'play.html')
            elif form == 'quiz_result':
                  self.end = time()
                  values = request.POST.dict()
                  win = self.chek_winers(values)
                  GamePageView.run_game.context['quiz'] = GamePageView.run_game.make_quiz()
                  self.start = time()
                  if GamePageView.rounds >= 3 :
                        GamePageView.run_game.score['home_name'] = GamePageView.run_game.context['squads']['home']['name']
                        GamePageView.run_game.score['ospit_name'] = GamePageView.run_game.context['squads']['ospit']['name']
                        GamePageView.run_game.make_output()
                        values=GamePageView.run_game.score.copy()
                        GamePageView.run_game = None
                        GamePageView.rounds = 0
                        context={'values':values}
                        win_page=reverse('winer',kwargs={'values':values})
                        print(context)
                        return HttpResponseRedirect(win_page)  #redirect(win_page, values=context)#render(request, 'winer.html',context)#HttpResponseRedirect(win_page,{'values':values}) #redirect(win_page,permanent=False,kwargs={'values':values})       
                  return render(request,'play.html',GamePageView.run_game.context)
            else:
                  return None


      def chek_winers(self, result:dict):
            quiz=eval(result["quiz"])
            res = GamePageView.run_game.ok_quiz(**quiz)
            GamePageView.rounds += 1
            GamePageView.run_game.score['rounds'][GamePageView.rounds] = dict()
            GamePageView.run_game.score['rounds'][GamePageView.rounds]['quiz']=quiz
            GamePageView.run_game.score['rounds'][GamePageView.rounds]['res'] = res
            GamePageView.run_game.score['rounds'][GamePageView.rounds]['winners'] = []
            have_win=0
            for k,v in result.items():
                  winer = dict()
                  if   k.startswith('player') and v.isnumeric() and int(v) == res:
                        have_win=1
                        win = k.split('-')
                        team = win[0].replace('player_', '')
                        winer['player'] = Players.objects.get(id=int(win[1]))
                        winer['time'] = (self.end - self.start) * 1000
                        GamePageView.run_game.sign_point(**winer)
                        GamePageView.run_game.score[team] += 1
                        GamePageView.run_game.score['rounds'][GamePageView.rounds]['winners'].append(winer)
                  else:
                        pass
            if have_win==0:
                  GamePageView.run_game.score['rounds'][GamePageView.rounds]['winners'].append('No player gave the correct answer in this round')
                        
            return True


      def get_players(self, teams):
            try:
                  squads={}
                  if Registrator.search(Teams,{'name':teams['home']}) and Registrator.search(Teams,{'name':teams['ospit']}):
                        players_home = Players.objects.filter(team__name__exact=teams['home'])
                        players_ospit = Players.objects.filter(team__name__exact=teams['ospit'])
                        squads['home'] = {'name':teams['home'], 'players':players_home}
                        squads['ospit'] = {'name':teams['ospit'],'players':players_ospit}           
                        GamePageView.run_game = PlayGame()
                        GamePageView.run_game.start_game(teams['home'], teams['ospit'])
                        return {'squads':squads}
                  raise djError('Teams not funds in our database')
            except djError as e:
                  print(e)
                  return None
            

class PlayPageView(TemplateView):
      template_name = "play.html"
      run_game=PlayGame()
      def get_context_data(self,values):
            print(values)
            squads=self.get_players(values)
            if squads is not None:
                  self.run_game.start_game(values['home'], values['ospit'])
            print(squads)
            context={'squads':squads}
            return context
      
      
class WinerPageView(TemplateView):
      template_name = "winer.html"
"""      def get_context_data(self,values):
            print(values)
            return values"""

def aboutPageView(request):
      url_home=reverse("home")
      page=f"""

<!DOCTYPE html>
<html lang="en">
<head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
</head>
<body>
   <a href={url_home}>home page</a> 
      
</body>
</html>



"""
      return HttpResponse(page)


#<!DOCTYPE html>
#<html lang="en">
#<head>
#      <meta charset="UTF-8">
#      <meta name="viewport" content="width=device-width, initial-scale=1.0">
#      <title>Document</title>
#</head>
#<body>


#</body>
#</html>