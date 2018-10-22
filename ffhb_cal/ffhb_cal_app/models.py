# Create your models here.
from django.db import models


class Departement(models.Model):
    code = models.IntegerField(default=1)
    nom = models.CharField(max_length=200, default='')


class Region(models.Model):
    code = models.IntegerField(default=1)
    nom = models.CharField(max_length=200, default='')


class Club(models.Model):
    name = models.CharField(max_length=200, default='')
    poule = models.CharField(max_length=200, default='')
    # default behaviour, if i delete departement, i delete the club
    departement = models.ForeignKey(
        Departement, on_delete=models.CASCADE, default=1)
    # default behaviour, if i delete departement, i delete the club
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    # Examples of model fields
    #models.DateTimeField('date published')
    #models.ForeignKey(Question, on_delete=models.CASCADE)
    # models.CharField(max_length=200)
    # models.IntegerField(default=0)

    # TODO : Ecrire les classes par défaut des modèles (save, init ...)

    """ def get_name_type_agenda(self, type_agenda):

        Idée d'utilisation du type agenda, ce champ permet de déterminer quel agenda page web on a affaire
        TODO : Enlever si pas utilisé

        agenda_types = {
            1: 'ffhb_style',
            2: 'hbcn_special',
            3: 'd1_ffhb'
            #4: '...'
        }
        return agenda_types[type_agenda] """


class ICSFile(models.Model):
    url = models.CharField(max_length=500, default='')
    name = models.CharField(max_length=200, default='')
    date_last_saved = models.DateTimeField('date of the last save')


class Poule(models.Model):
    start_date = models.DateTimeField(
        'date of the start of the poule', default='')
    end_date = models.DateTimeField('date of the end of the poule', default='')
    url = models.CharField(max_length=500, default='')
    type_agenda = models.CharField(max_length=100, default='')
    type_club = models.CharField(max_length=100, default='')  # dep,reg,nation
    division = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=200, default='')
    url = models.OneToOneField(ICSFile, default=1, on_delete=models.CASCADE)


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
        related_name='exterieur',
        default=1)
    score_club_domicile = models.IntegerField(default=0)
    score_club_exterieur = models.IntegerField(default=0)
    # Qui va nous permettre de distinguer les matchs pas encore prévus dans le
    # calendrier
    type_date = models.CharField(max_length=50, default='')
    date = models.DateTimeField('date of the game', default='')
    localisation = models.CharField(max_length=200, default='')
    url_feuille_match = models.CharField(max_length=500, default='')


class Joueur(models.Model):
    nom = models.CharField(max_length=200, default='')
    nb_goals = models.IntegerField(default=0)
    nb_matches = models.IntegerField(default=0)
    average = models.FloatField(default=0.0)


class ClubJoueur (models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=1)
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE, default=1)
    date_end_club = models.DateTimeField(
        'date end of this player in this club', default='')
    # Useful to detect if the player has switched club or not
    # FIXME : Not clear how to say this player played for this club during this time
    # Not ideal, need to find another idea


class Buts(models.Model):
    date = models.DateTimeField('date of the scored goal', default='')
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE, default=1)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default=1)
