
from .models import Teams, Players, Profiles,Games, Gols_Scored
from django.utils import timezone
from random import randint, choice
from collections import Counter

now =timezone.now()


class PlayGame:

      def __init__(self):
            self.home_team=None
            self.ospit_opponent=None
            self._game=None
            self.context=None
            self.score = {'home':0, 'ospit':0, 'rounds':dict()}

      def start_game(self,home_team, opponent,date=now):
            self.home_team=Teams.objects.get(name=home_team)
            self._game = Games.objects.create(team=self.home_team,game_date=date,opponent=opponent)
            self._game.save()

      def sign_point(self,player, time):
            point_data={'game':self._game, 'minute':time, 'player':player}
            point= Gols_Scored.objects.create(**point_data)
            point.save()
            

      def end_game(self):
            self._game.score=f"{self.score['home']} - {self.score['ospit']}"
            self._game.save()

      def make_output(self):
            tit="The winner team is {}".format('')
            if self.score['home'] > self.score['ospit'] :
                  tit.format(self.score['home_name']) 
            elif self.score['home'] < self.score['ospit'] :
                  tit.format(self.score['ospit_name'])
            elif self.score['home'] == self.score['ospit'] :
                  tit = "This game finisch with a parity"
            points=f"{tit}<br>{self.score['home_name']} {self.score['home']} - {self.score['ospit']} {self.score['ospit_name']}"
            self.score['result_title'] = points
            tot=[]
            goals=Gols_Scored.objects.filter(game=self._game)
            for team in self.context['squads'].values() :
                  for player in team['players'] :
                        goal_player = len(goals.filter(player=player))
                        tot.append((goal_player, player))
            top =sorted(tot,key=lambda x: x[0])
            self.score['top'] = top


      @staticmethod
      def make_quiz():
            simbol = choice(['+', '-', '*', '/'])
            n1, n2 = randint(1,21), randint(1,21)
            if PlayGame.ok_quiz(n1, simbol, n2) is False:
                  return PlayGame.make_quiz()
            return {'n1':n1, 'simbol':simbol,'n2':n2}

      @staticmethod
      def ok_quiz(n1, simbol, n2):
            res=0
            if simbol== '/':
                  res = n1 / n2
            elif simbol == '*':
                  res = n1 * n2
            elif simbol == '+':
                  res = n1 + n2
            elif simbol == '-':
                  res = n1 - n2
            print(isinstance(res, int), res<0 )
            if isinstance(res, int) and res > 0:
                  return res
            return False