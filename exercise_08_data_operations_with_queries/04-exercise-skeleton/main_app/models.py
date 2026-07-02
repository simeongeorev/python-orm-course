from django.db import models

# Create your models here.
# 01
class Pet(models.Model):
    name = models.CharField(max_length=40)
    species = models.CharField(max_length=40)

# 02
class Artifact(models.Model):
    name = models.CharField(max_length=70)
    origin = models.CharField(max_length=70)
    age = models.PositiveIntegerField()
    description = models.TextField()
    is_magical = models.BooleanField(default=False)

# 03
class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    population = models.PositiveIntegerField()
    description = models.TextField()
    is_capital = models.BooleanField(default=False)

# 04
class Car(models.Model):
    model = models.CharField(max_length=40)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_discount = models.DecimalField(max_digits=10,
                                              decimal_places=2,
                                              default=0)

# 05
class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(default=False)

# 06
class HotelRoom(models.Model):
    class RoomTypeChoices(models.TextChoices):
        STANDARD = "ST", "Standard"
        DELUXE = "DE", "Deluxe"
        SUITE = "SU", "Suite"

    room_number = models.PositiveIntegerField()
    room_type = models.CharField(max_length=10,
                                 choices=RoomTypeChoices.choices)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_reserved  = models.BooleanField(default=False)

# 07
class Character(models.Model):
    class ClassNames(models.TextChoices):
        MAGE = "Mage"
        WARRIOR = "Warrior"
        ASSASSIN = "Assassin"
        SCOUT = "Scout"

    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20,
                                  choices=ClassNames.choices)
    level = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    inventory = models.TextField()
