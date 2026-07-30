from django.db.models import Manager
from django.db.models.aggregates import Count


class ProfileManager(Manager):
    def get_regular_customers(self):
        return (self
                .annotate(orders_count=Count('order'))
                .filter(orders_count__gt=2)
                .order_by('-orders_count'))