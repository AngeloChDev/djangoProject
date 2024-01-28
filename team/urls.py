from django.urls import path
from .views import ( 
    HomePageView, 
    aboutPageView, 
    TeamsPageView, 
    AllPlayersPageView, 
    HomePlayerPageView,
    GamePageView,
    PlayPageView,
    WinerPageView)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("teams/", TeamsPageView.as_view(), name="teams"),
    path("all&Players/", AllPlayersPageView.as_view(), name="all_players"),
    path("all&Players/<int:player_id>", HomePlayerPageView.as_view(), name="home_player"),
    path("about/",aboutPageView, name="about" ),
    path("game/",GamePageView.as_view(), name="game" ),
    path("winer/",WinerPageView.as_view(), name="winer" ),
    
]