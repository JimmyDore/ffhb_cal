# Create your models here.
from django.db import models


class Competition(models.Model):  # First page ffhb
    nom = models.CharField(max_length=200, default='')
    url = models.CharField(max_length=500, default='')
    type = models.CharField(max_length=3, default='')  # Nat, Dep, ou Reg


class PouleGen(models.Model):
    nom = models.CharField(max_length=200, default='')
    url = models.CharField(max_length=500, default='')
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, default=1)


class Poule(models.Model):
    # ID du groupe qu'on peut retrouver sur la feuille de match
    ffhb_id = models.CharField(max_length=30, default='')
    start_date = models.DateTimeField(
        'date of the start of the poule', default='')
    end_date = models.DateTimeField('date of the end of the poule', default='')
    url = models.CharField(max_length=500, default='')
    # Nom du championnat dans la barre défilante
    name = models.CharField(max_length=200, default='')
    poule_gen = models.ForeignKey(
        PouleGen, on_delete=models.CASCADE, default=1)
    last_updated_classement = models.DateTimeField(
        'date parsing of the ranking teams', default='')
    last_updated_buteurs = models.DateTimeField(
        'date parsing of the ranking scorers', default='')


class Departement(models.Model):
    code = models.IntegerField(default=1)
    nom = models.CharField(max_length=200, default='')


class Region(models.Model):
    code = models.IntegerField(default=1)
    nom = models.CharField(max_length=200, default='')


class ICSFile(models.Model):
    url = models.CharField(max_length=500, default='')
    name = models.CharField(max_length=200, default='')
    date_last_saved = models.DateTimeField('date of the last save')


class Club(models.Model):
    name = models.CharField(max_length=200, default='')
    poule = models.CharField(max_length=200, default='')
    departement = models.ForeignKey(
        Departement, on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    ics_file = models.OneToOneField(
        ICSFile, default=1, on_delete=models.CASCADE)
    # Examples of model fields
    #models.DateTimeField('date published')
    #models.ForeignKey(Question, on_delete=models.CASCADE)
    # models.CharField(max_length=200)
    # models.IntegerField(default=0)

    # TODO : Ecrire les classes par défaut des modèles (save, init ...)


class Classement(models.Model):
    poule = models.ForeignKey(Poule, default=1, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, default=1, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    pts = models.IntegerField(default=0)
    nb_matchs = models.IntegerField(default=0)
    nb_wins = models.IntegerField(default=0)
    nb_lost = models.IntegerField(default=0)
    nb_draw = models.IntegerField(default=0)
    nb_goals_scored = models.IntegerField(default=0)
    nb_goals_taken = models.IntegerField(default=0)
    diff = models.IntegerField(default=0)


class Joueur(models.Model):
    ffhb_id = models.CharField(max_length=200, default='')  # Licence
    nom = models.CharField(max_length=200, default='')
    nb_goals = models.IntegerField(default=0)
    nb_matches = models.IntegerField(default=0)
    average = models.FloatField(default=0.0)


class ClassementButeurs(models.Model):
    poule = models.ForeignKey(Poule, default=1, on_delete=models.CASCADE)
    joueur = models.ForeignKey(Joueur, default=1, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, default=1, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    nb_games = models.IntegerField(default=0)
    nb_goals = models.IntegerField(default=0)
    average = models.IntegerField(default=0)


class Match(models.Model):
    club_domicile = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='domicile',
        default=1)
    club_exterieur = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='exterieur',
        default=1)
    poule = models.ForeignKey(
        Poule,
        on_delete=models.CASCADE,
        default=1)
    score_club_domicile = models.IntegerField(default=0)
    score_club_exterieur = models.IntegerField(default=0)
    # type_date : va nous permettre de distinguer les matchs pas encore prévus dans le
    # calendrier
    type_date = models.CharField(max_length=50, default='')
    date = models.DateTimeField('date of the game', default='')
    localisation = models.CharField(max_length=200, default='')
    last_updated = models.DateTimeField(
        'date last_parsing of the game', default='')
    url_feuille_match = models.CharField(max_length=500, default='')
    parsing_feuille_match = models.BooleanField(default=False)


class Actions(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        default=1)
    name = models.CharField(max_length=200, default='')
    joueur = models.ForeignKey(Joueur, default=1, on_delete=models.CASCADE)
    # Tir, arrêt, But ...
    action = models.CharField(max_length=200, default='')
    time = models.DateTimeField('datetime of the action', default='')
    score = models.CharField(max_length=200, default='')


class Buts(models.Model):
    date = models.DateTimeField('date of the scored goal', default='')
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE, default=1)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default=1)
