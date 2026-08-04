from django.db.models import Manager
from django.db.models.aggregates import Count


class HouseManager(Manager):
    def get_houses_by_dragons_count(self):
        return (
            self.annotate(dragons_count=Count('dragon'))
            .order_by('-dragons_count', 'name')
        )
