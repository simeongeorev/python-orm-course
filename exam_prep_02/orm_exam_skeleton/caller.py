import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, Sum, F, Avg
from datetime import date


# 04 ---

def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ""

    filtered_astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not filtered_astronauts.exists():
        return ""

    return "\n".join(
        f"Astronaut: {x.name}, phone number: {x.phone_number}, status: {'Active' if x.is_active else 'Inactive'}"
        for x in filtered_astronauts
    )


def get_top_astronaut() -> str:
    top_astronaut = (
        Astronaut.objects
        .get_astronauts_by_missions_count()
        .filter(missions_count__gt=0)
        .first()
    )

    if not top_astronaut:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."


def get_top_commander() -> str:
    top_commander = (
        Astronaut.objects
        .annotate(commandments=Count('commanded_missions'))
        .filter(commandments__gt=0)
        .order_by('-commandments', 'phone_number')
        .first()
    )

    if not top_commander:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.commandments} commanded missions."


# 05 ---

from django.db.models import Sum


def get_last_completed_mission():
    latest_mission = (
        Mission.objects
        .filter(status=Mission.StatusChoices.COMPLETED)
        .order_by('-launch_date')
        .first()
    )

    if not latest_mission:
        return "No data."

    commander_name = latest_mission.commander.name if latest_mission.commander else "TBA"

    astronauts_list = ", ".join(
        a.name for a in latest_mission.astronauts.order_by('name')
    )

    # Safely extract the integer sum (defaulting to 0 if None)
    total_spacewalks = (
        latest_mission.astronauts
        .aggregate(Sum('spacewalks'))['spacewalks__sum']  # aggregate dict
    )

    return (
        f"The last completed mission is: {latest_mission.name}. "
        f"Commander: {commander_name}. "
        f"Astronauts: {astronauts_list}. "
        f"Spacecraft: {latest_mission.spacecraft.name}. "
        f"Total spacewalks: {total_spacewalks}."
    )


def get_most_used_spacecraft():
    top_spacecraft = (
        Spacecraft.objects
        .annotate(
            missions_count=Count('mission'),
            astronauts_count=Count('mission__astronauts', distinct=True)
            # The 'astronauts on missions' represent the number of unique astronauts who have been on missions with this spacecraft.
        )
        .filter(missions_count__gt=0)  # If no missions exist in the database, return the following string: "No data."
        .order_by('-missions_count', 'name')
        .first()
    )

    if not top_spacecraft:
        return "No data."

    return (
        f"The most used spacecraft is: {top_spacecraft.name}, "
        f"manufactured by {top_spacecraft.manufacturer}, "
        f"used in {top_spacecraft.mission_set.count()} missions, "
        f"astronauts on missions: {top_spacecraft.astronauts_count}."
    )


def decrease_spacecrafts_weight():
    spacecrafts = (
        Spacecraft.objects
        .distinct()
        .annotate(num_missions=Count('mission'))
        .filter(
            num_missions__gt=0,
            mission__status=Mission.StatusChoices.PLANNED,
            weight__gte=200.0
        )
        .update(weight=F('weight') - 200.0)
    )

    if spacecrafts < 1:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(Avg('weight'))['weight__avg']

    return (
        f"The weight of {spacecrafts} "
        f"spacecrafts has been decreased. "
        f"The new average weight of all spacecrafts is {avg_weight:.1f}kg"
    )

# def create_test_data():
#     # Clear existing data to avoid conflicts during testing
#     Mission.objects.all().delete()
#     Astronaut.objects.all().delete()
#     Spacecraft.objects.all().delete()
#
#     # --- Create Astronauts ---
#     john = Astronaut.objects.create(
#         name="John Deer",
#         is_active=True,
#         spacewalks=3,
#         date_of_birth=date(1980, 1, 1),
#         phone_number="853967"
#     )
#
#     jane = Astronaut.objects.create(
#         name="Jane Smith",
#         is_active=True,
#         spacewalks=1,
#         date_of_birth=date(1985, 5, 15),
#         phone_number="123456"
#     )
#
#     josie = Astronaut.objects.create(
#         name="Josie Stam",
#         is_active=False,
#         spacewalks=0,
#         date_of_birth=date(1990, 3, 12),
#         phone_number="111111"
#     )
#
#     # --- Create Spacecrafts ---
#     explorer_1 = Spacecraft.objects.create(
#         name="Explorer I",
#         manufacturer="SpaceTech Inc.",
#         capacity=5,
#         launch_date=date(2022, 1, 1),
#         weight=12000.5
#     )
#
#     explorer_2 = Spacecraft.objects.create(
#         name="Explorer II",
#         manufacturer="SpaceX",
#         capacity=2,
#         launch_date=date(2023, 5, 1),
#         weight=10000.2
#     )
#
#     # --- Create Missions ---
#     # Mission 1
#     m1 = Mission.objects.create(
#         name="Moon Landing",
#         status=Mission.StatusChoices.PLANNED,
#         launch_date=date(2024, 10, 10),
#         description="Aimed at landing on the moon",
#         commander=john,
#         spacecraft=explorer_1
#     )
#     m1.astronauts.set([john, jane])
#
#     # Mission 2
#     m2 = Mission.objects.create(
#         name="Moon Landing2",
#         status=Mission.StatusChoices.COMPLETED,
#         launch_date=date(2024, 3, 1),
#         description="Aimed at landing on the moon",
#         commander=josie,
#         spacecraft=explorer_1
#     )
#     m2.astronauts.set([jane, josie])
#
#     print("Test data successfully created!")
#
#
# # Run function to populate DB
# create_test_data()
