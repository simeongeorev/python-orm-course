from django.db.models import Manager, Count, Avg

from querysets import RealEstateListingQuerySet, VideoGameQuerySet

# 01 ---

class RealEstateListingManager(Manager.from_queryset(RealEstateListingQuerySet)):
    def popular_locations(self):
        return self.values('location') \
            .annotate(location_count=Count('location')) \
            .order_by('-location_count', 'location')[:2]


# 02 ---

class VideoGameManager(Manager.from_queryset(VideoGameQuerySet)):
    def highest_rated_game(self):
        return self.order_by('-rating').first()

    def lowest_rated_game(self):
        return self.order_by('rating').first()

    def average_rating(self):
        return f"{self.aggregate(avg_rating=Avg('rating'))['avg_rating']:.1f}"

# 03 ---

# class InvoiceManager(Manager.from_queryset(InvoiceQuerySet)):
#     def get_invoice_with_billing_info(self, invoice_number: str):
#         return self.get(invoice_number=invoice_number)

