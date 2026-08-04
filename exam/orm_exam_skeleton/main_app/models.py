from datetime import date

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import CASCADE

from managers import HouseManager


# Create your models here.
class NameMixin(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)],
        unique=True
    )

    class Meta:
        abstract = True


class ModifiedAtMixin(models.Model):
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class House(NameMixin, ModifiedAtMixin, models.Model):
    motto = models.TextField(null=True, blank=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(max_length=80, null=True, blank=True)
    wins = models.PositiveSmallIntegerField(default=0)

    objects = HouseManager()


class Dragon(NameMixin, ModifiedAtMixin, models.Model):
    class Breaths(models.TextChoices):
        FIRE = "Fire"
        ICE = "Ice"
        LIGHTNING = "Lightning"
        UNKNOWN = "Unknown"

    power = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        default=1.0
    )
    breath = models.CharField(max_length=9, choices=Breaths, default=Breaths.UNKNOWN)
    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField(default=date.today)
    wins = models.PositiveSmallIntegerField(default=0)
    house = models.ForeignKey(to=House, on_delete=CASCADE)


class Quest(NameMixin, ModifiedAtMixin, models.Model):
    code = models.CharField(max_length=4,
                            validators=[RegexValidator(regex=r"^[A-Za-z#]{4}$")],
                            unique=True)
    reward = models.FloatField(default=100.0)
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(to=Dragon)
    host = models.ForeignKey(to=House, on_delete=CASCADE)
