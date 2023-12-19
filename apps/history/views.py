from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.channel.views import suscription
from apps.channel.models import Channel, Video
from .models import History
from django.utils import timezone



ONE_DAY_SECONDS = 24 * 60 * 60
MOMENT_DAYS_LIST = [i * ONE_DAY_SECONDS for i in range(8)][::-1]
MOMENT_DAYS_TEXT = (['Hoy','Ayer'] + [f'Hace {(i+3)} días' for i in range(5)] + ['Hace más de una semana'])[::-1]

class HistoryView(LoginRequiredMixin, View):
    login_url = '/account/google/login/'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        channel = Channel.objects.get(user=request.user)
        history = History.objects.filter(channel=channel, videos__title__icontains=query)

        context = {}
        context['channel'] = channel

        if history:
            history = history.get()
            videos_history = []
            for i in range(len(MOMENT_DAYS_LIST)):
                dic = {}
                dic['videos'] = []
                for video in history.videos.all():
                    deltadate = timezone.now() - video.created_at
                    if deltadate.seconds >= MOMENT_DAYS_LIST[i]:
                        dic['moment'] = MOMENT_DAYS_TEXT[i]
                        dic['videos'].append(video)
                if len(dic['videos']) > 0:
                    videos_history.append(dic)
            context['history'] = videos_history
            
        else:
            context['history'] = False

        suscription(request, context)
        return render(request, template_name='pages/history/index.html', context=context)



class ClearHistory(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        channel = Channel.objects.get(user=request.user)
        context = {}
        context['channel'] = channel
        return render(request, template_name='modals/clear-history.html', context=context)

    def post(self, request, *args, **kwargs):
        history = History.objects.get(channel__user=request.user)
        history.videos.clear()
        history.save()
        return redirect('/feed/history/')
    


class TogglePauseHistory(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        channel = Channel.objects.get(user=request.user)
        context = {}
        context['channel'] = channel
        return render(request, template_name='modals/pause-history.html', context=context)
    
    def post(self, request, *args, **kwargs):
        channel = Channel.objects.get(user=request.user)
        channel.is_paused_history = not channel.is_paused_history
        channel.save()
        return redirect('/feed/history/')
    


class RemoveFromHistory(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(pk=kwargs['pk'])
        history = History.objects.get(channel__user=request.user)
        history.videos.remove(video)
        history.save()
        return redirect('/feed/history/')



history_view = HistoryView.as_view()
clear_history = ClearHistory.as_view()
toggle_pause_history = TogglePauseHistory.as_view()
remove_from_history = RemoveFromHistory.as_view()