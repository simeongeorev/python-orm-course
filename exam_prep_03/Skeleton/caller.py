import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Count


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None) -> str:
    if search_name is None and search_country is None:
        return ""

    if search_name is not None and search_country is not None:
        result = TennisPlayer.objects.filter(
            full_name__icontains=search_name,
            country__icontains=search_country
        ).order_by('ranking')

    elif search_name is not None and search_country is None:
        result = TennisPlayer.objects.filter(
            full_name__icontains=search_name
        ).order_by('ranking')

    elif search_name is None and search_country is not None:
        result = TennisPlayer.objects.filter(
            country__icontains=search_country
        ).order_by('ranking')

    if not result.exists():
        return ""

    return "\n".join(f"Tennis Player: {x.full_name}, country: {x.country}, ranking: {x.ranking}"
                     # better to leave the strings on one line
                     for x in result)


def get_top_tennis_player() -> str:
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not top_player or top_player.wins_count == 0:  # don't forget to check if there are any wins
        return ""

    return (f"Top Tennis Player: {top_player.full_name} "
            f"with {top_player.wins_count} wins.")


def get_tennis_player_by_matches_count() -> str:
    top_player = (
        TennisPlayer.objects
        .annotate(num_matches=Count('matches'))
        .order_by('-num_matches', 'ranking')
        .first()
    )

    if not top_player or top_player.num_matches == 0:  # don't forget to check if there are any matches
        return ""

    return (f"Tennis Player: {top_player.full_name} "
            f"with {top_player.num_matches} matches played.")


def get_tournaments_by_surface_type(surface=None) -> str:
    if surface is None:
        return ""

    tournaments = (
        Tournament.objects
        .annotate(num_matches=Count('matches'))
        .filter(
            surface_type__icontains=surface,
            num_matches__gt=0  # check if it's needed
        )
        .order_by('-start_date')
    )

    if not tournaments.exists():
        return ""

    return "\n".join(
        f"Tournament: {x.name}, start date: {x.start_date}, matches: {x.num_matches}"
        for x in tournaments)


def get_latest_match_info():
    latest_match = (
        Match.objects
        .order_by('-date_played', '-id')
        .first()
    )

    if not latest_match:
        return ""

    date_played = latest_match.date_played.date()
    tournament_name = latest_match.tournament.name
    score = latest_match.score
    players = (
        " vs "
        .join(
            x.full_name for x in latest_match.players.order_by('full_name')
        )
    )
    # winner =

def get_matches_by_tournament(tournament_name=None):
    ...
