from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models
from django.db.models import CASCADE, SET_NULL

from managers import AstronautManager


# Create your models here.
class NameMixin(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])

    class Meta:
        abstract = True


class LaunchDateMixin(models.Model):
    launch_date = models.DateField()

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Astronaut(NameMixin, UpdatedAtMixin, models.Model):
    phone_number = models.CharField(max_length=15,
                                    unique=True,
                                    validators=[
                                        RegexValidator(regex=r'^\d+$')
                                    ])

    is_active = models.BooleanField(default=True)

    date_of_birth = models.DateField(null=True,
                                     blank=True)

    spacewalks = models.IntegerField(default=0,
                                     validators=[
                                         MinValueValidator(0)
                                     ])

    objects = AstronautManager()

class Spacecraft(NameMixin, LaunchDateMixin, UpdatedAtMixin, models.Model):
    manufacturer = models.CharField(max_length=100)

    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    weight = models.FloatField(validators=[MinValueValidator(0.0)])


class Mission(NameMixin, LaunchDateMixin, UpdatedAtMixin, models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = "Planned"
        ONGOING = "Ongoing"
        COMPLETED = "Completed"

    description = models.TextField(null=True,
                                   blank=True)

    status = models.CharField(choices=StatusChoices,
                              max_length=9,
                              default=StatusChoices.PLANNED)

    spacecraft = models.ForeignKey(to="Spacecraft",
                                   on_delete=CASCADE)

    astronauts = models.ManyToManyField(to="Astronaut",
                                        related_name="missions")

    commander = models.ForeignKey(to="Astronaut",
                                  on_delete=SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name="commanded_missions")

