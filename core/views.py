from django.shortcuts import render
from django.views import View
from allauth.socialaccount.models import SocialAccount
from apps.channel.models import Channel, Video


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:    
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            channel_logged = Channel.objects.get(user=request.user, is_active=True)

            suscriptions = []
            for channel in channel_logged.suscribers.all():
                suscription = {}
                suscription['channel_username'] = channel.user.username
                suscription['channel_fullname'] = channel.user.get_full_name()
                suscription['channel_avatar_url'] = \
                    SocialAccount.objects.get(user=channel.user, provider='google').get_avatar_url()
                suscriptions.append(suscription)

            context['avatar_url'] = social_account.get_avatar_url()
            context['user'] = request.user
            context['suscriptions'] = suscriptions
            
        context['videos'] = Video.objects.all()
        return render(request, template_name='pages/home/index.html', context=context)
