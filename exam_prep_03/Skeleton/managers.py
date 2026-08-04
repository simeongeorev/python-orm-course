from django.db.models import Manager, Count

class TennisPlayerManager(Manager):
    def get_tennis_players_by_wins_count(self):
         return (
             self.annotate(wins_count=Count('won_matches'))
             .order_by('-wins_count', 'full_name')
         )

