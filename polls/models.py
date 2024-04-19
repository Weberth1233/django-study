import datetime

from django.db import models
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        print(timezone.now() - datetime.timedelta(days=1))
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text

class Musican(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

    def __str__(self) -> str:
        return  f'{self.first_name} - {self.last_name} - {self.instrument}'
    
class Album(models.Model):
    artist = models.ForeignKey(Musican, on_delete=models.CASCADE, verbose_name="related album with musican")
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_starts = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.name} - {self.release_date} - {self.num_starts} '
    

#Relacionamento 1 para muitos
class Manufacturer(models.Model):
    #Criando um campo com o tamanho maximo de 50 e unico(Não podendo se repetir)
    name_company = models.CharField(max_length=50,unique = True)

    def __str__(self):
        return f'Nome da companhia = {self.name_company}'

class Car(models.Model):
    #Um modelo de carro pode ser de um fabricante - Manufacture uma fabricante pode fazer vários carros 
    company_that_makes_it = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name_car = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.company_that_makes_it.name_company, self.name_car}'

    
# Relacionamento M(muitos) para M(muitos)
#from polls.models import *
# >>> ringo = Person.objects.create(name="Ringo Starr")
# >>> paul = Person.objects.create(name="Paul McCartney")
# >>> beatles = Group.objects.create(name="The Beatles")
# >>> m1 = Membership(
# ...     person=ringo,
# ...     group=beatles,
# ...     date_joined=date(1962, 8, 16),
# ...     invite_reason="Needed a new drummer.",
# ... )
# >>> m1.save()
# >>> beatles.members.all()
# <QuerySet [<Person: Ringo Starr>]>
# >>> ringo.group_set.all()
# <QuerySet [<Group: The Beatles>]>
# >>> m2 = Membership.objects.create(
# ...     person=paul,
# ...     group=beatles,
# ...     date_joined=date(1960, 8, 1),
# ...     invite_reason="Wanted to form a band.",
# ... )
# >>> beatles.members.all()
# <QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>

#Outras formas de adicionar no grupo:
#beatles.members.create(name="George Harrison", through_defaults ={"date_joined": timezone.now()})

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    #O modelo intermediário está associado a 
    #ManyToManyField usando o argumento through para apontar para o modelo 
    #que atuará como um intermediário.
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self) -> str:
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete= models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

