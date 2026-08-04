import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, F
from main_app.models import House, Dragon, Quest
from django.db.models.aggregates import Min, Avg
from decimal import Decimal

# Create queries within functions
def get_houses(search_string=None):
    if search_string is None or search_string == "":
        return "No houses match your search."

    houses = House.objects.filter(
        Q(name__istartswith=search_string) |
        Q(motto__istartswith=search_string)
    ).order_by('-wins', 'name')

    if not houses.exists():
        return "No houses match your search."

    return "\n".join(f"House: {x.name}, wins: {x.wins}, motto: {x.motto if x.motto else 'N/A'}"
                     for x in houses)

def get_most_dangerous_house():
    top_house = House.objects.get_houses_by_dragons_count().first()

    if not top_house or top_house.dragons_count == 0:
        return "No relevant data."

    return (
        f"The most dangerous house is the House of {top_house.name} with {top_house.dragons_count} dragons. Currently {'ruling' if top_house.is_ruling else 'not ruling'} the kingdom."
    )

def get_most_powerful_dragon():
    top_dragon = Dragon.objects.annotate(num_quests=Count('quest')).filter(is_healthy=True).order_by('-power', 'name').first()

    if not top_dragon:
        return "No relevant data."

    return f"The most powerful healthy dragon is {top_dragon.name} with a power level of {top_dragon.power:.1f}, breath type {top_dragon.breath}, and {top_dragon.wins} wins, coming from the house of {top_dragon.house.name}. Currently participating in {top_dragon.num_quests} quests."


def update_dragons_data():
    num_of_dragons_affected = Dragon.objects.filter(
        is_healthy=False, power__gte=1.1
    ).update(power=F('power') - Decimal('0.1'), is_healthy=True)

    if num_of_dragons_affected == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    return f"The data for {num_of_dragons_affected} dragon/s has been changed. The minimum power level among all dragons is {min_power:.1f}"


def get_earliest_quest():
    quest = Quest.objects.order_by('start_time').first()

    if not quest:
        return "No relevant data."

    day = quest.start_time.day
    month = quest.start_time.month
    year = quest.start_time.year
    host_name = quest.host.name

    dragons_qs = quest.dragons.order_by('-power', 'name')
    dragons = "*".join(x.name for x in dragons_qs)
    avg_power_level = f"{dragons_qs.aggregate(avg_power=Avg('power'))['avg_power']:.2f}"

    return f"The earliest quest is: {quest.name}, code: {quest.code}, start date: {day}.{month}.{year}, host: {host_name}. Dragons: {dragons}. Average dragons power level: {avg_power_level}"


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code__exact=quest_code).first()

    if not quest:
        return "No such quest."

    dragon_winner = quest.dragons.order_by('-power', 'name').first()

    dragon_winner.wins += 1
    dragon_winner.save()

    dragon_winner.house.wins += 1
    dragon_winner.house.save()

    result = f"The quest: {quest.name} has been won by dragon {dragon_winner.name} from house {dragon_winner.house.name}. The number of wins has been updated as follows: {dragon_winner.wins} total wins for the dragon and {dragon_winner.house.wins} total wins for the house. The house was awarded with {quest.reward:.2f} coins."

    quest.delete()

    return result
