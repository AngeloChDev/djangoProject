from django.urls import path
from .views import ( 
    HomePageView, 
    aboutPageView, 
    delete_team,
    TeamsPageView, 
    AllPlayersPageView, 
    InfoPlayerPageView,
    GamePageView,
    PlayPageView,
    WinerPageView,
    PointsPageView,
    TeamInfoPageView)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("teams/", TeamsPageView.as_view(), name="teams"),
    path("all&Players/", AllPlayersPageView.as_view(), name="all_players"),
    path("all&Players/<int:player_id>", InfoPlayerPageView.as_view(), name="info_player"),
    path("about/",aboutPageView, name="about" ),
    path("game/",GamePageView.as_view(), name="game" ),
    path("winer/",WinerPageView.as_view(), name="winer" ),
    path("deleteteam/<team_id>",delete_team, name="team_deleter" ),
    path("points/",PointsPageView.as_view(), name="points_page" ),
     path("teams/teamInfo/<int:team_id>",TeamInfoPageView.as_view(), name="team_info_page" ),
    
]