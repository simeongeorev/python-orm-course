from decimal import Decimal

from django.db.models import QuerySet

# 01 ---

class RealEstateListingQuerySet(QuerySet):
    def by_property_type(self, property_type: str) -> QuerySet:
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        return self.filter(price__range=[min_price, max_price])

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        return self.filter(bedrooms=bedrooms_count)

# 02 ---

class VideoGameQuerySet(QuerySet):
    def games_by_genre(self, genre: str) -> QuerySet:
        return self.filter(genre=genre)

    def recently_released_games(self, year: int) -> QuerySet:
        return self.filter(release_year__gte=year)

# 03 ---

# class InvoiceQuerySet(QuerySet):
#
#     def get_invoices_with_prefix(self, prefix: str):
#         return self.filter(invoice_number__startswith=prefix)
#
#     def get_invoices_sorted_by_number(self):
#         return self.order_by('invoice_number')




