from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE
from django.dispatch import receiver


# Create your models here.
# 01 ---
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)

# 02 ---
class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)

class Message(models.Model):
    sender = models.ForeignKey(to="UserProfile",
                               related_name="sent_messages",
                               on_delete=CASCADE)
    receiver = models.ForeignKey(to="UserProfile",
                                 related_name="received_messages",
                                 on_delete=CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self) -> None:
        self.is_read = True

    def reply_to_message(self, reply_content: str) -> 'Message':
        new_message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content,
        )
        new_message.save()
        return new_message

    def forward_message(self, receiver: UserProfile) -> 'Message':
        new_message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content,
        )
        new_message.save()
        return new_message

# 03 ---
class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value):
        try:
            return super().to_python(value)
        except ValidationError:
            raise ValueError("Invalid input for student ID")

    def get_prep_value(self, value):
        value = self.to_python(value)

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return value

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()

# 04 ---

class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")
        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"



class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()


# 05 ---

# Model Hotel
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


# Model Room
class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=CASCADE,
        related_name="rooms"
    )
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    