POSTGRES USER 
postgres-user

POSTGRES PASSWORD
password

	-1 Create venv:
	python -m venv .myenv

	-2 activate the venv
	.\.myenv\Scripts\activate
	
	-3 change the psycopg version in the requirements file to:
	psycopg2-binary>=2.9.12

	-4 install the project requirements
	pip install -r requirements.txt
	
	-5 start docker postgresql
	
	-6 create new DB connection to PostgreSQL
	
	-7 create new Database inside it
	
	-8 in the settings.py -> use the created Postgre DB and delete/comment the old sqlite3 setting
	
	-9 make the first migration
	python manage.py makemigrations
	python manage.py migrate
	
	-10 test if the Django app can be started
	python manage.py runserver

- install Django
pip install Django

- start the Django app / run server
python manage.py runserver

- migrate the changes
python manage.py makemigrations

- execute the migration
python manage.py migrate

- create a super user (admin)
python manage.py createsuperuser

- list the applied migrations: 
python manage.py showmigrations -l

- print the generated SQL code: 
python manage.py sqlmigrate main_app 0001_initial

- make empty migration
python manage.py makemigrations main_app --name migrate_unique_brands --empty

- go to a specific migration: 
python manage.py migrate main_app 0001


- manage python versions 
pyenv versions
pyenv local {version}
pyenv global {version}
pyenv install --list


- install IPython if not included in the local env
pip install ipython

- run the django shell command:
python manage.py shell


Django Models
ORM - Object Relational Mapping
Django models

Всеки модел е отделна таблица
Всяка променлова използваща поле от models е колона в тази таблица
Моделите ни позволяват да не ни се налага писането на low level SQL
Създаване на модели

Наследяваме models.Model
Migrations

makemigrations
migrate
Други команди

dbshell - отваря конзола, в която можем да пишем SQL
CTRL + ALT + R - отваря manage.py console
Migrations and Admin
Django Migrations Advanced

Миграциите ни помагат надграждаме промени в нашите модели
Както и да можем да пазим предишни стейтове на нашата база
Команди:
makemigrations
migrate
Връщане до определена миграция - migrate main_app 0001
Връщане на всички миграции - migrate main_app zero
showmigrations - показва всички апове и миграциите, които имат
showmigrations app_name - показва миграциите за един app
showmigrations --list - showmigrations -l
squashmigrations app_name migration_to_which_you_want_to_sqash - събира миграциите до определена миграция в една миграция
sqlmigrate app_name migration_name - дава ни SQL-а на текущата миграция - използваме го, за да проверим дали миграцията е валидна
makemigrations --empty main_app - прави празна миграция в зададен от нас app
Custom/Data migrations

Когато например добавим ново поле, искаме да го попълним с данни на база на вече съществуващи полета, използваме data migrations

RunPython

викайки функция през него получаваме достъп до всички апове и техните модели (първи параметър), Scheme Editor (втори параметър)
добра практика е да подаваме фунцкия и reverse функция, за да можем да връщаме безпроблемно миграции
Scheme Editor - клас, който превръща нашия пайтън код в SQL, ползваме го когато правим create, alter и delete на таблица

използвайки RunPython в 95% от случаите няма да ни се наложи да ползавме Scheme Editor, освен, ако не правим някаква временна таблица индекси или промяна на схемата на таблицата
Стъпки:

2.1. Създаваме празен файл за миграция: makemigrations --empty main_app - прави празна миграция в зададен от нас app

2.2. Дефиниране на операции - Използваме RunPython за да изпълним data migrations

2.3. Прилагане на промените - migrate

Пример с временна таблица:

Да приемем, че имате модел с име „Person“ във вашето Django приложение и искате да създадете временна таблица, за да съхранявате някои изчислени данни въз основа на съществуващите данни в таблицата „Person“. В този случай можете да използвате мигриране на данни, за да извършите тази операция:

Create the Data Migration:
Run the following command to create a data migration:

python manage.py makemigrations your_app_name --empty
This will create an empty data migration file.

Edit the Data Migration:
Open the generated data migration file and modify it to use RunPython with a custom Python function that utilizes the SchemaEditor to create a temporary table. Here's an example:

from django.db import migrations, models

def create_temporary_table(apps, schema_editor):
    # Get the model class
    Person = apps.get_model('your_app_name', 'Person')

    # Access the SchemaEditor to create a temporary table
    schema_editor.execute(
        "CREATE TEMPORARY TABLE temp_person_data AS SELECT id, first_name, last_name FROM your_app_name_person"
    )

    ...

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', 'previous_migration'),
    ]

    operations = [
        migrations.RunPython(create_temporary_table),
    ]
Django admin

createsuperuser
Register model, example:
   @admin.register(OurModelName)
   class OurModelNameAdmin(admin.ModelAdmin):
	pass
Admin site customizations

str метод в модела, за да го визуализираме в админ панела по-достъпно

list_display - Показваме различни полета още в админа Пример:

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ['job_title', 'first_name', 'email_address']
List filter - добавя страничен панел с готови филтри Пример:

 class EmployeeAdmin(admin.ModelAdmin):
 	list_filter = ['job_level']
Searched fields - казваме, в кои полета разрешаваме да се търси, по дефолт са всички Пример:

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['email_address']
Layout changes - избираме, кои полета как и дали да се появяват при добавяне или промяна на запис Пример:

class EmployeeAdmin(admin.ModelAdmin):
    fields = [('first_name', 'last_name'), 'email_address']
list_per_page

fieldsets - променяме визуално показването на полетата Пример:

  fieldsets = (
       ('Personal info',
        {'fields': (...)}),
       ('Advanced options',
        {'classes': ('collapse',),
       'fields': (...),}),
  )
Data Operations in Django with queries
CRUD overview

CRUD - Create, Read, Update, Delete
Използваме го при:
Web Development
Database Management
Дава ни един консистентен начин, за това ние да създаваме фунцкионалност за CRUD
Можем да го правим през ORM-a на Джанго
Мениджър в Django:

Атрибут на ниво клас на модел за взаимодействия с база данни.
Отговорен за CRUD
Custom Manager: Подклас models.Manager.
Защо персонализирани мениджъри:
Капсулиране на общи или сложни заявки.
Подобрена четимост на кода.
Избягвайме повторенията и подобряваме повторната употреба.
Промяна наборите от заявки според нуждите.
Django Queryset

QuerySet - клас в пайтън, които изпозваме, за да пазим данните от дадена заявка

Данните не се взимат, докато не бъдат потърсени от нас

cars = Cars.objects.all() # <QuerySet []>

print(cars) # <QuerySet [Car object(1)]>

QuerySet Features:

Lazy Evaluation - примера с колите, заявката не се вика, докато данните не потрябват
Retrieving objects - можем да вземаме всички обекти или по даден критерии
Chaining filters - MyModel.objects.filter(category='electronics').filter(price__lt=1000)
query related objects - позволява ни да търсим в таблици, с които имаме релации, през модела: # Query related objects using double underscores related_objects = Order.objects.filter(customer__age__gte=18)
Ordering - ordered_objects = Product.objects.order_by('-price')
Pagination
 from django.core.paginator import Paginator

  # Paginate queryset with 10 objects per page
  paginator = Paginator(queryset, per_page=10)
  page_number = 2
  print([x for x in paginator.get_page(2)])
Django Simple Queries

Object Manager - default Objects
Methods:
all()
first()
get(**kwargs)
create(**kwargs)
filter(**kwargs)
order_by(*fields)
delete()
Django Shell and SQL Logging

Django Shell
Дава ни достъп до целия проект
python manage.py shell
SQL logging
Enable SQL logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Other levels CRITICAL, ERROR, WARNING, INFO, DEBUG
    },
    'loggers': {
        'django.db.backends': {  # responsible for the sql logs
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
Working with queries
Working with Queries

Useful Methods

filter() - връща subset от обекти; приема kwargs; връща queryset;
exclude() - връща subset от обекти; приема kwargs; връща queryset;
order_by() - връща сортираните обекти; - за desc;
count() - като len, но по-бързо; count връща само бройката без да му трябвата реалните обекти;
get() - взима един обект по даден критерии;
Chaning methods

всеки метод работи с върнатия от предишния резултат
Lookup keys

Използват се във filter, exclude, get;
__exact __iexact - матчва точно;
__contains __icontains - проверява дали съдържа;
__startswith __endswith
__gt __gte
__lt __lte
__range=(2, 5) - both inclusive
Bulk methods

използват се за да извършим операции върху много обекти едновременно
bulk_create - създава множество обекти навъеднъж;
filter().update()
filter().delete()
Django Relations
Django Models Relations

Релации в Django Модели
Получават се използвайки ForeignKey полета

related_name - можем да направим обартна връзка

По дефолт тя е името + _set
Пример:

class Author(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
Access all posts written by an author
author = Author.objects.get(id=1)
author_posts = author.post_set.all()
Types of relationships

Many-To-One (One-To-Many)

Many-To-Many

Няма значение, в кой модел се слага
Django автоматично създава join таблица или още наричана junction
Но, ако искаме и ние можем да си създадем:
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, through='AuthorBook')

class AuthorBook(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publication_date = models.DateField()
OneToOne, предимно се слага на PK

Self-referential Foreign Key

Пример имаме работници и те могат да са мениджъри на други работници
class Employee(models.Model):
    name = models.CharField(max_length=100)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
Lazy Relationships - обекта от релацията се взима, чрез заявка, чак когато бъде повикан

Models Inheritance and Customization
Типове наследяване

Multi-table
Разширяваме модел с полетата от друг модел, като не копираме самите полета, а използваме създадения от django pointer, който прави One-To-One Relationship
Пример:
class Person(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    def is_student(self):
        """Check if this person is also a student."""
        return hasattr(self, 'student')

class Student(Person):
    student_id = models.CharField(max_length=15)
    major = models.CharField(max_length=50)
Abstract Base Classes

При това наследяване не се създават две нови таблици, а само една и тя е на наследяващия клас(Child), като абстрактния клас(Parent) е само шаблон
Постигаме го чрез промяна на Meta класа:
class AbstractBaseModel(models.Model):
    common_field1 = models.CharField(max_length=100)
    common_field2 = models.DateField()

    def common_method(self):
        return "This is a common method"

    class Meta:
        abstract = True
Proxy Models

Използваме ги, за да добавим функционалност към модел, който не можем да достъпим
Можем да добавяме методи, но не и нови полета
Пример:
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()

class RecentArticle(Article):
    class Meta:
        proxy = True

    def is_new(self):
        return self.published_date >= date.today() - timedelta(days=7)
    
    @classmethod
    def get_recent_articles(cls):
        return cls.objects.filter(published_date__gte=date.today() - timedelta(days=7))
Основни Built-In Методи

save() - използва се за запазване на записи
    def save(self, *args, **kwargs):
        # Check the price and set the is_discounted field
        if self.price < 5:
            self.is_discounted = True
        else:
            self.is_discounted = False

        # Call the "real" save() method
        super().save(*args, **kwargs)
clean() - използва се, когато искаме да валидираме логически няколко полета, например имаме тениска в 3 цвята, но ако е избран XXL цветовете са само 2.
Custom Model Properties

Както и в ООП, можем чрез @property декоратора да правим нови атрибути, които в случая не се запазват в базата
Използваме ги за динамични изчисления на стойностти
Custom Model Fields

Ползваме ги когато, Django няма field, които ни върши работа
Имаме методи като:
from_db_value - извиква се, когато искаме да взмем стойността от базата в пайтън
to_python - извиква се когато правим десериализация или clean
get_prep_value - обратното на from_db_value, от Python към базата, предимно ползваме за сериализации
pre_save - използва се за last minute changes, точно преди да запазим резултата в базата

class RGBColorField(models.TextField):
    # Convert the database format "R,G,B" to a Python tuple (R, G, B)
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    # Convert any Python value to our desired format (tuple)
    def to_python(self, value):
        if isinstance(value, tuple) and len(value) == 3:
            return value
        if isinstance(value, str):
            return tuple(map(int, value.split(',')))
        raise ValidationError("Invalid RGB color format.")

    # Prepare the tuple format for database insertion
    def get_prep_value(self, value):
        # Convert tuple (R, G, B) to "R,G,B" for database storage
        return ','.join(map(str, value))
		
Advanced Django Models Techniques
Validation in Models
Built-in Validators
MaxValueValidator, MinValueValidator - приема два аргумета (limit, message)
MaxLengthValidator, MinLengthValidator - приема два аргумета (limit, message)
RegexValidator - приема два аргумета (regex, message)
class SampleModel(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)]  # Name should have a minimum length of 5 characters
    )

    age = models.IntegerField(
        validators=[MaxValueValidator(120)]  # Assuming age shouldn't exceed 120 years
    )

    phone = models.CharField(
        max_length=15,
        validators=[
	    RegexValidator(
	        regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
	)]  # A simple regex for validating phone numbers
    )
Custom Validators - функции, които често пишем в отделен файл. При грешка raise-ваме ValidationError
Meta Options and Meta Inheritance

В мета класа можем да променяме:
Името на таблицата
Подреждането на данните
Можем да задаваме constraints
Можем да задаваме типа на класа(proxy, abstract)
class SampleModel(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()

    class Meta:
        # Database table name
        db_table = 'custom_sample_model_table'

        # Default ordering (ascending by name)
        ordering = ['name'] - Случва се на SELECT, не на INSERT

        # Unique constraint (unique combination of name and email)
        unique_together = ['name', 'email']
Meта наследяване:
Ако наследим абстрактен клас и не презапишем мета класа, то наслеяваме мета класа на абстрактния клас
class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        abstract = True
        ordering = ['name']

class ChildModel(BaseModel):
    description = models.TextField()
    # ChildModel inherits the Meta options
Indexing

Индексирането ни помага, подреждайки елементите в определен ред или създавайки друга структура, чрез, която да търсим по-бързо.
Бързо взимаме записи, но ги запазваме по-бавно
В Django можем да сложим индекс на поле, като добавим key-word аргумента db_index=True
Можем да направим и индекс, чрез мета класа, като можем да правим и композитен индекс
class Meta:
indexes=[
models.Index(fields=["title", "author"]),  # прави търсенето по два критерия, по-бързо
models.Index(fields=["publication_date"])
]
Django Model Mixins

Както знаем, миксините са класове, които използваме, за да отделим обща функционалност
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	class Meta:
    	    abstract = True
			
