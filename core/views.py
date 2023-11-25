from django.shortcuts import render
from django.views import View
from allauth.socialaccount.models import SocialAccount
from apps.channel.models import Channel, Video
from apps.channel.views import suscription


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        suscription(request, context)
            
        context['videos'] = Video.objects.all()
        return render(request, template_name='pages/home/index.html', context=context)
