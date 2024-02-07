from django import template
from ..models import Players, Teams
register = template.Library()

@register.filter
def hide_obj(x , ):
      if x==1:
            x='on_form'
            return
      x='no_display'            
      return
      


@register.filter
def ox(y):
      print(y)

@register.filter
def lop(data):
      l=[]
      for i, j in zip(data,range(1,len(data ) + 1)):
            
            x = f"""<span class='rounds'> -  Round {j} -</span> <br>
            Quiz : {i['quiz']['n1']} {i['quiz']['simbol']} {i['quiz']['n2']} <br>
            Correct result : {i['res']}<br>          
            Players who answered correctly :<br>"""
            p=[]
            for winner in i['winners']:
                  
                  if isinstance(winner, str):
                        x += winner
                  else:
                        x += f"<span class='rounds'>  - </span>  {winner['player'].player}  {winner['player'].team.name} <br>"
                        
            
            x += "<hr class='line'><br>"
            l.append(x)
      return ''.join(l)     

@register.filter
def lop_winet_team(winers:dict):
      out=[]
      for winer in winers:
            print(winer)
            v= list(winer[1].values())
            out.append(f"<li class='white fs-3 m-1 p-1'>The team {list(winer)[0].name} has obtained {v[0]} winned  and  {v[1]}  tied</li><br>")
      return "".join(out)