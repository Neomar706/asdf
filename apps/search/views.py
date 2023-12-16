from django.shortcuts import render
from django.views import View
from django.db.models import Q
from apps.channel.models import Channel, Video
from apps.channel.views import suscription
from django.utils import timezone

class SearchVideos(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        filter = request.GET.get('filter', '')
        channel = Channel.objects.get(user=request.user, is_active=True)
        deltadate = timezone.now() - timezone.timedelta(days=1)

        flag, videos, filterobj = False, None, {}
        match filter:
            case 'viewed':
                filterobj['views'] = channel
            case 'unviewed':
                flag = True
                videos = Video.objects.filter(Q(title__icontains=query) | 
                                              Q(channel__name__icontains=query), 
                                              ~Q(views=channel))
            case 'recent':
                filterobj['created_at__gte'] = deltadate
            case 'suscriptions':
                filterobj['channel__suscribers'] = channel

        if not flag:
            videos = Video.objects.filter(Q(title__icontains=query) | 
                                          Q(channel__name__icontains=query), **filterobj)

        context = {}
        suscription(request, context)

        context['videos'] = videos.all()
        context['deltadate'] = deltadate
        
        return render(request, template_name='pages/search/index.html', context=context)


search_videos = SearchVideos.as_view()