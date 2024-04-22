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
#-------------------------------------------------------
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
#---------------------------------------------------------
#Relacionamento 1 para 1
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name} o local"
    
class Restaurant(models.Model):
    #O restaurante está em apenas um local
    place = models.OneToOneField(
        Place, on_delete=models.CASCADE,
        primary_key = True
    )
    server_hot_dogs = models.BooleanField(default=False)
    server_pizza = models.BooleanField(default=False)

    def __str__(self):
        return '%s O restaurante' % self.place.name
    
class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s O Garçom %s" % (self.name, self.restaurant)
#---------------------------------------------------------
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
#------------------------------------------------------------  
# Relacionamento M(muitos) para M(muitos)
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

