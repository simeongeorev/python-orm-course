import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from decimal import Decimal
from django.db.models.functions import Mod
from django.db.models import F


# Create queries within functions
# 01
def create_pet(name, species):
    Pet.objects.create(name=name, species=species)

    return f"{name} is a very cute {species}!"


# print(create_pet("Buddy", "Dog"))
# print(create_pet("Whiskers", "Cat"))

# 02
def create_artifact(name: str,
                    origin: str,
                    age: int,
                    description: str,
                    is_magical: bool):
    Artifact.objects.create(name=name,
                            origin=origin,
                            age=age,
                            description=description,
                            is_magical=is_magical)

    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword',
#                       'Lost Kingdom',
#                       500,
#                       'A legendary sword with a rich history',
#                       True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)
# delete_all_artifacts()

# 03
def show_all_locations():
    all_locs = Location.objects.all().order_by("-id")
    result = [f"{loc.name} has a population of {loc.population}!" for loc in all_locs]
    return "\n".join(result)


def new_capital():
    # as a queryset with data only for the name of the location
    Location.objects.filter(id=Location.objects.first().id).update(is_capital=True)


def get_capitals():
    return Location.objects.filter(is_capital=True).values("name")


def delete_first_location():
    first_loc = Location.objects.first()
    if first_loc:
        first_loc.delete()


# Location.objects.create(name="Sofia",
#                         region="Sofia Region",
#                         population=1329000,
#                         description="The capital of Bulgaria and the largest city in the country",
#                         is_capital=False)
#
# Location.objects.create(name="Plovdiv",
#                         region="Plovdiv Region",
#                         population=346942,
#                         description="The second-largest city in Bulgaria with a rich historical heritage",
#                         is_capital=False)
#
# Location.objects.create(name="Varna",
#                         region="Varna Region",
#                         population=330486,
#                         description="A city known for its sea breeze and beautiful beaches on the Black Sea",
#                         is_capital=False)

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

# 04
def apply_discount():
    all_cars = Car.objects.all()

    for c in all_cars:
        discount = sum(int(digit) for digit in str(c.year))
        multiplier = Decimal((100 - discount) / 100)  # converts to Decimal
        c.price_with_discount = c.price * multiplier

    Car.objects.bulk_update(all_cars, ['price_with_discount'])  # bulk update


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values("model", "price_with_discount")


def delete_last_car():
    last_car = Car.objects.last()
    if last_car:
        last_car.delete()


# bulk create
# Car.objects.bulk_create(
#     [
#         Car(model="Mercedes C63 AMG", year=2019, color="white", price=120000.00),
#         Car(model="Audi Q7 S line", year=2023, color="black", price=183900.00),
#         Car(model="Chevrolet Corvette", year=2021, color="dark grey", price=199999.00),
#     ]
# )

# apply_discount()
# print(get_recent_cars())


# 05
def show_unfinished_tasks():
    all_incomplete_tasks = Task.objects.filter(is_finished=False)
    return "\n".join(f"Task - {t.title} needs to be done until {t.due_date}!" for t in all_incomplete_tasks)


def complete_odd_tasks():
    # all_tasks = Task.objects.all()
    # for t in all_tasks:
    #     if t.id % 2 != 0:
    #         t.is_finished=True
    # Task.objects.bulk_update(all_tasks, ["is_finished"])

    Task.objects.annotate(id_mod=Mod("id", 2)).filter(id_mod=1).update(is_finished=True)


def encode_and_replace(text: str, task_title: str):
    def encode(word: str) -> str:
        return "".join(chr(ord(c) - 3) for c in word)

    Task.objects.filter(title=task_title).update(description=encode(text))


# Task.objects.create(
#     title="Sample Task",
#     description="This is a sample task description",
#     due_date="2023-10-31",
#     is_finished=False
# )
#
# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title='Sample Task').description)

# 06
def get_deluxe_rooms():
    filtered_rooms = (HotelRoom.objects
                      .filter(room_type="DE")
                      .annotate(mod_id=Mod("id", 2))
                      .filter(mod_id=0))

    return "\n".join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!"
        for r in filtered_rooms)


def increase_room_capacity():
    rooms = list(HotelRoom.objects.all().order_by("id"))

    if not rooms:
        return

    first_room = rooms[0]

    if first_room:
        if first_room.room_type == "RE":
            first_room.capacity += first_room.id

    for i in range(1, len(rooms)):
        if rooms[i].room_type == "RE":
            rooms[i].capacity += rooms[i - 1].capacity

    HotelRoom.objects.bulk_update(rooms, ["capacity"])


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    if first_room:
        first_room.is_reserved = True
        first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room and not last_room.is_reserved:
        last_room.delete()


# rooms_to_create = [
#     HotelRoom(room_number=401, room_type="ST", capacity=2, amenities="Tv" , price_per_night=Decimal("100.00")),
#     HotelRoom(room_number=501, room_type="DE", capacity=3, amenities="Wi-Fi", price_per_night=Decimal("200.00")),
#     HotelRoom(room_number=601, room_type="DE", capacity=6, amenities="Jacuzzi" , price_per_night=Decimal("400.00")),
# ]
#
# HotelRoom.objects.bulk_create(rooms_to_create)

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)

# 07
def update_characters():
    Character.objects.filter(class_name=Character.ClassNames.MAGE).update(
        level=F("level") + 3,
        intelligence=F("intelligence") - 7
    )
    # for m in mages:
    #     m.level += 3
    #     m.intelligence -= 7
    # Character.objects.bulk_update(mages, ["level", "intelligence"])

    Character.objects.filter(class_name=Character.ClassNames.WARRIOR).update(
        hit_points=F("hit_points") / 2,
        dexterity=F("dexterity") + 4
    )
    # for w in warriors:
    #     w.hit_points = int(w.hit_points / 2)
    #     w.dexterity += 4
    # Character.objects.bulk_update(warriors, ["hit_points", "dexterity"])

    Character.objects.filter(class_name__in=[Character.ClassNames.ASSASSIN, Character.ClassNames.SCOUT]).update(
        inventory="The inventory is empty")
    # for c in scouts_and_assassins:
    #     c.inventory = "The inventory is empty"
    # Character.objects.bulk_update(scouts_and_assassins, ["inventory"])


def fuse_characters(first_character: Character, second_character: Character):
    new_inventory = ""
    if first_character.class_name in [Character.ClassNames.MAGE, Character.ClassNames.SCOUT]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [Character.ClassNames.WARRIOR, Character.ClassNames.ASSASSIN]:
        new_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=f"{first_character.name} {second_character.name}",
        class_name="Fusion",
        level=int((first_character.level + second_character.level) // 2),
        strength=int((first_character.strength + second_character.strength) * 1.2),
        dexterity=int((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=int((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=first_character.hit_points + second_character.hit_points,
        inventory=new_inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def grand_strength():
    Character.objects.all().update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()


character1 = Character.objects.create(
    name='Gandalf',
    class_name='Mage',
    level=10,
    strength=15,
    dexterity=20,
    intelligence=25,
    hit_points=100,
    inventory='Staff of Magic, Spellbook',
)

character2 = Character.objects.create(
    name='Hector',
    class_name='Warrior',
    level=12,
    strength=30,
    dexterity=15,
    intelligence=10,
    hit_points=150,
    inventory='Sword of Troy, Shield of Protection',
)

fuse_characters(character1, character2)
fusion = Character.objects.filter(class_name='Fusion').get()

print(fusion.name)
print(fusion.class_name)
print(fusion.level)
print(fusion.intelligence)
print(fusion.inventory)
