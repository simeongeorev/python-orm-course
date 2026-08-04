from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from managers import TennisPlayerManager


class SurfaceChoices(models.TextChoices):
    NOT_SELECTED = "Not Selected", "Not Selected"
    CLAY = "Clay", "Clay"
    GRASS = "Grass", "Grass"
    HARD_COURT = "Hard Court", "Hard Court"


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5)]
    )
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(300)
        ]
    )
    is_active = models.BooleanField(
        default=True
    )

    objects = TennisPlayerManager()


class Tournament(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    start_date = models.DateField()
    surface_type = models.CharField(
        max_length=12,
        choices=SurfaceChoices,
        default=SurfaceChoices.NOT_SELECTED
    )


class Match(models.Model):
    score = models.CharField(
        max_length=100
    )
    summary = models.TextField(
        validators=[MinLengthValidator(5)]
    )
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    players = models.ManyToManyField(
        to=TennisPlayer,
        related_name='matches'
    )
    winner = models.ForeignKey(
        to=TennisPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_matches'
    )

    class Meta:
        verbose_name_plural = "Matches"