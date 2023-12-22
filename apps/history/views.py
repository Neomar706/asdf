from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.channel.views import suscription
from apps.channel.models import Channel, Video
from .models import History
from django.utils import timezone


MOMENT_DAYS_TEXT = ['Hace más de una semana'] + [f'Hace {(7-i)} días' for i in range(5)] + ['Ayer', 'Hoy']

def get_moment(seconds):
    ONE_DAY_SECONDS = 24 * 60 * 60
    MOMENT_DAYS_LIST = [(7-i) * ONE_DAY_SECONDS for i in range(8)]

    index = -1
    for i, moment in enumerate(MOMENT_DAYS_LIST):
        if seconds >= moment:
            index = i

    return MOMENT_DAYS_TEXT[index]


class HistoryView(LoginRequiredMixin, View):
    login_url = '/account/google/login/'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        channel = Channel.objects.get(user=request.user)
        history = History.objects.filter(channel=channel, video__title__icontains=query)

        context = {}
        context['channel'] = channel

        if history:
            videos_history = [{'moment': m, 'videos': []} for m in MOMENT_DAYS_TEXT][::-1]
            for his in history:
                deltadate = timezone.now() - his.created_at
                moment = get_moment(deltadate.seconds)
                history_index = next((index for index, dic in enumerate(videos_history) if dic['moment'] == moment), None)
                videos_history[history_index]['videos'].append(his.video)

            videos_history = [i for i in videos_history if len(i['videos'])]
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
        history = History.objects.filter(channel__user=request.user)
        for his in history:
            his.delete()
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
        history = History.objects.get(channel__user=request.user, video=video)
        history.delete()
        return redirect('/feed/history/')



history_view = HistoryView.as_view()
clear_history = ClearHistory.as_view()
toggle_pause_history = TogglePauseHistory.as_view()
remove_from_history = RemoveFromHistory.as_view()