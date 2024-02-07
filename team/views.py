from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_level, get_messages
from django.urls import reverse
from django.views.generic.base import TemplateView
from team.registration import Registrator, djError
from .models import Teams, Players, Profiles,Games, Gols_Scored
from markupsafe import Markup
from collections import Counter
from time import time
from .game import PlayGame
from .forms import TeamsModelForm, PlayersModelForm
from .more_settings import CARDS, PAGES
from .utils import full_dict



class HomePageView(TemplateView):
      template_name = "home.html"
      #Registrator.upload_defoult()
      #Registrator.add_profile_toplayer(1,{'height':10, 'weight':70,'nationality':'Deutchland'})
      def get_context_data(self,   *args, **kwargs):
            context={
                  "home_cards":CARDS["home_cards"], 
                  "home_cards_class":CARDS["classes"],
                  "detail":PAGES["home"],
                  "detail_class":PAGES["classes"]}
            return context
            
class TeamsPageView(TemplateView):
      template_name="teams.html"
      form= TeamsModelForm

      def get_context_data(self):
            teams = Teams.objects.all()
            context = {
                  "detail":PAGES["teams"],
                  "detail_class":PAGES["classes"],
                  "teams": teams,
                  "card_class":CARDS["classes"] , 
                  "form":self.form
                  }
            return context
      
      def post(self, request, *args, **kwargs):
            
            try:
                  recived_form = self.form(request.POST)
                  if recived_form.is_valid():
                        recived_form.save()
                        messages.success(request,"New Team created","new_team")
                        
                        return redirect('home')
                  raise djError('Team name already exists')
            except djError as e:
                  messages.error(request,"Error team name exist","new_team")
                  return redirect('home')




class AllPlayersPageView(TemplateView):
      template_name = "all_players.html"
      form =PlayersModelForm


      def get_context_data(self):
            players = Players.objects.all()
            context = {
                  "detail":PAGES["players"],
                  "detail_class":PAGES["classes"],
                  "players": players,
                  "form":self.form,
                  }
            return context
      def post(self, request, *args, **kwargs):
            
            try:
                  recived_form = self.form(request.POST)
                  x=recived_form.is_valid()
                  if x:
                        messages.success(request,"New player added","new_team")
                        return redirect('home')
                  raise djError('Player name already exists')
            except djError as e:
                  messages.error(request,"Error player name exist","new_team")
                  return redirect('home')
      

class InfoPlayerPageView(TemplateView):
      template_name = "info_player.html"
      form =PlayersModelForm
      def get_context_data(self,player_id):
            old=[]
            players = Players.objects.all()
            info_player = Players.objects.get(id=player_id)
            for k,v in info_player.old_teams.items():
                  if isinstance(v, int) or v.isnumeric():
                        team=Teams.objects.get(id=v)
                  else:
                        team=Teams.objects.get(name=v)
                  old.append({'year':k,'team':team})
            context = {"players": players, 
                        "info_player":info_player,
                        "old":old,"form":self.form,
                        "detail":PAGES["players"],
                        "detail_class":PAGES["classes"],
                       }
            return context
      
      def post(self, request, *args, **kwargs):
            return AllPlayersPageView().post(request, *args, **kwargs)

class PointsPageView(TemplateView):
      template_name="point.html"

      def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            all_points=Gols_Scored.objects.all()
            ranked={}
            for point in all_points:
                  if point.player not in list(ranked.keys()):
                        ranked[point.player]=0
                  ranked[point.player] += 1
            ord = sorted(ranked.items(),key=lambda x:x[1],reverse=True)
            all_game = Games.objects.all()
            wined = {}
            for game in all_game:
                  if game.score:
                        score = game.score.split('-')
                        if score[0] > score[1]:
                              winer= [game.team]
                        elif score[1] > score[0]:
                              winer= [Teams.objects.get(name=game.opponent)]
                        else:
                              winer=[game.team, Teams.objects.get(name=game.opponent)]

                        wined = full_dict(winer, wined)
            
            
            ord_winers = sorted(list(wined.items()),key=lambda x:x[1]['w'],reverse=True)
            context={
                  'rank_players':ord,
                  "detail":PAGES["points"],
                  "detail_class":PAGES["classes"],
                  "winer_team":ord_winers,
                  }
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
                  if GamePageView.rounds >= 2 :
                        GamePageView.run_game.score['home_name'] = GamePageView.run_game.context['squads']['home']['name']
                        GamePageView.run_game.score['ospit_name'] = GamePageView.run_game.context['squads']['ospit']['name']
                        GamePageView.run_game.make_output()
                        values=GamePageView.run_game.score.copy()
                        GamePageView.run_game = None
                        GamePageView.rounds = 0
                        context={'values':values}
                        return render(request,'winer.html', context) #render(request, 'winer.html', context) #HttpResponseRedirect(win_page)  #redirect(win_page, values=context)#render(request, 'winer.html',context)#HttpResponseRedirect(win_page,{'values':values}) #redirect(win_page,permanent=False,kwargs={'values':values})       
                  return render(request,'play.html',GamePageView.run_game.context)
            else:
                  return None


      def chek_winers(self, result:dict):
            quiz=eval(result["quiz"])
            res = GamePageView.run_game.ok_quiz(**quiz)
            GamePageView.rounds += 1
            rounds=dict()
            rounds['quiz']=quiz
            rounds['res'] = res
            rounds['winners'] = []
            #GamePageView.run_game.score['rounds'][GamePageView.rounds] = dict()
            #GamePageView.run_game.score['rounds'][GamePageView.rounds]['quiz']=quiz
            #GamePageView.run_game.score['rounds'][GamePageView.rounds]['res'] = res
            #GamePageView.run_game.score['rounds'][GamePageView.rounds]['winners'] = []
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
                        rounds['winners'].append(winer)
                        #GamePageView.run_game.score['rounds'][GamePageView.rounds]['winners'].append(winer)
                  else:
                        pass
            if have_win==0:
                  #GamePageView.run_game.score['rounds'][GamePageView.rounds]['winners'].append('No player gave the correct answer in this round')
                  rounds['winners'].append('No player gave the correct answer in this round')      
            GamePageView.run_game.score['rounds'].append(rounds)
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
            squads=self.get_players(values)
            if squads is not None:
                  self.run_game.start_game(values['home'], values['ospit'])
            context={'squads':squads}
            return context
      


class TeamInfoPageView(TemplateView):
      template_name = "team_info.html"
      form = TeamsModelForm
      def get_context_data(self,team_id):
            try:
                  if  team_id:
                        team = Teams.objects.get(id=team_id)
                        players=Players.objects.filter(team=team)
                        games_home = Games.objects.filter(team=team)
                        games_ospit = Games.objects.filter(opponent=team.name)
                        context={'form':self.form,
                              "detail":PAGES["team_info"],
                              "detail_class":PAGES["classes"],  
                              "team":team,
                              "players":players,
                              "games_home":games_home,
                              "games_ospit":games_ospit,
                              }
                        return context
                  raise djError('Value error')
            except djError as e:
                  print(e)
                  return None
            
      def post(self,request, *args, **kwargs):
            return TeamsPageView().post(request, *args, **kwargs)


class WinerPageView(TemplateView):
      template_name = "winer.html"

      
      """      def get_context_data(self,values):
            print(values)
            return values"""


      
def delete_team(request, team_id):
      team=Teams.objects.get(id=team_id)
      try:
            team.delete()
            messages.success(request,"Team Deleted" , "del_team")
            return redirect('home')
      except:
            messages.error(request,f"Error deleting this team {team.name}" , "del_team")
            return redirect('home')



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


