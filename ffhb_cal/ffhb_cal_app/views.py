from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse
from django.views.generic import View
from .scrap_calendar import generateICS

class Home(View):
    """
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'ffhb_cal_app/index.html')

    def post(self, request):
        #TODO : Need function who gets id of club, get url associated, send it to the scrap_calendar
        if(generateICS("http://hbcnantes.com/equipe-professionnelle/equipe-pro-calendrier/")):
            print('lol')
            context = {'clubname': request.POST['clubname']}
            print('lol')
            #TODO : Avec l'id du club, on prend le nom du fichier ics associé (model) et on construit l'url qu'on envoie dans le contexte

            return render(request, 'ffhb_cal_app/index.html', context)
        else:
            print('ol')
            context = {'clubname': request.POST['clubname']}
            print('ol')
            return render(request, 'ffhb_cal_app/index.html', context)