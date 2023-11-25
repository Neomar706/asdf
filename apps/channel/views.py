from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Channel, Video, Playlist
from .forms import AddVideoForm, AddPlaylistForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from moviepy.editor import VideoFileClip
from datetime import timedelta
from apps.playlist.models import Playlist
from urllib.parse import unquote
from json import loads as load_json


class ChannelView(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['user'])
        channel = Channel.objects.get(user=user)
        account_channel = SocialAccount.objects.get(user=user, provider='google')

        context = {}
        context['channel'] = channel

        self.suscription(context, channel)

        if not self.channel_tabs(context, **kwargs):
            return HttpResponse('404 Página no encontrada')

        context['channel_avatar_url'] = account_channel.get_avatar_url()
        context['lorem'] = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora tenetur quaerat, non odit, at quibusdam et quas sint natus consequatur culpa nisi, ipsa assumenda consectetur tempore! Obcaecati non nisi voluptatum totam pariatur placeat eum consequuntur dolore nemo deleniti fuga minus mollitia perspiciatis eos reiciendis, neque enim esse, officia magnam optio illo sunt ipsa ea? Tempora numquam voluptates, veritatis molestias commodi voluptatibus obcaecati optio animi, fugit nihil fuga ad mollitia consectetur quasi magnam beatae. Veniam officia quasi, consectetur sunt assumenda perspiciatis, eos nemo asperiores consequuntur quidem inventore ipsum exercitationem id expedita deserunt at unde dolor voluptate accusantium maxime iusto dicta quod saepe ipsa? Quasi, totam obcaecati voluptatum veniam facilis voluptatem maxime odio corrupti explicabo ullam assumenda quidem rerum sit, excepturi necessitatibus dolor, ut omnis nam cumque? Officia consequatur id recusandae, hic, quia dicta voluptatibus fugiat beatae alias blanditiis deleniti, quo odit. Tempora totam ut officiis adipisci maxime? Nobis aut dolorem dignissimos cumque atque quisquam facilis cum dolore, similique totam molestias? Perferendis ratione quis deleniti cumque quasi, quas, suscipit explicabo quia similique unde sit minus! Laboriosam nobis nostrum harum tempora sequi eius. Omnis eaque corporis doloribus quos non, libero assumenda beatae quae nisi voluptatibus! Eaque cupiditate, quia, placeat ad beatae dolore necessitatibus iste ipsam reiciendis tempore dignissimos. Sint voluptatem sit nulla, molestiae consequuntur magni porro non impedit illo eveniet voluptas pariatur aut. Aliquid eum enim aut beatae pariatur accusamus placeat numquam eligendi sequi tenetur cumque non tempore id alias possimus laborum quas, ducimus ex dolorum eaque ea. Amet inventore accusamus corporis aliquam nemo temporibus impedit repellendus, nostrum sed accusantium quidem ad, deserunt sint enim. Maxime veniam eius ad velit voluptates animi et, maiores dolorem temporibus molestiae exercitationem, mollitia excepturi distinctio quibusdam necessitatibus rerum, magni repellendus sunt voluptatum hic. Cum, velit, quasi minima alias excepturi voluptatibus ut vero hic fugiat fugit, praesentium totam.'
        return render(request, template_name='pages/channel/index.html', context=context)

    def suscription(self, context, channel):
        request = self.request
        if request.user.is_authenticated:
            account_logged = SocialAccount.objects.get(user=request.user, provider='google')
            channel_logged = Channel.objects.get(user=request.user, is_active=True)

            suscriptions = []
            for ch in channel_logged.suscribers.all().order_by('id'):
                suscription = {}
                suscription['channel_username'] = ch.user.username
                suscription['channel_fullname'] = ch.user.get_full_name()
                suscription['channel_avatar_url'] = \
                    SocialAccount.objects.get(user=ch.user, provider='google').get_avatar_url()
                suscriptions.append(suscription)

            context['is_suscriber'] = True if channel_logged in channel.suscribers.all() else False
            context['logged_avatar_url'] = account_logged.get_avatar_url()
            context['suscriptions'] = suscriptions

    def channel_tabs(self, context, **kwargs):
        valid_tabs = ['main', 'videos', 'playlists', 'channels', 'info']
        if not kwargs['tab'] in valid_tabs:
            return False

        match kwargs['tab']:
            case 'videos':
                context['videos'] = Video.objects.filter(channel=context['channel']).order_by('-created_at')
            case 'playlists':
                context['playlists'] = Playlist.objects.filter(channel=context['channel']).order_by('-created_at')

        context['tab'] = kwargs['tab']
        return True


class AddVideo(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        playlists = Playlist.objects.filter(channel__user=request.user).values_list('pk', 'title')
        form = AddVideoForm()
        videos = Video.objects.filter(channel__user=request.user).all()

        playlists_list = []
        for playlist in playlists:
            pl = {}
            pl['pk'] = playlist[0]
            pl['title'] = playlist[1]
            playlists_list.append(pl)

        context = {}
        context['form'] = form
        context['playlists'] = playlists_list
        context['videos'] = videos
        print(playlists)
        return render(request, template_name='modals/add-video.html', context=context)

    def post(self, request, *args, **kwargs):
        channel = Channel.objects.get(user=request.user, is_active=True)          
        form = AddVideoForm(request.POST, request.FILES)
        playlist_pk = request.POST['playlist']
        final_screens_pks = request.POST['final_screens_ids']
        decode_uri  = unquote(final_screens_pks)
        data        = load_json(decode_uri)

        if form.is_valid():
            video = request.FILES['video']
            video_clip = VideoFileClip(video.temporary_file_path())
            video_duration = video_clip.duration

            new_video = form.save(commit=False)
            new_video.duration = timedelta(seconds=video_duration)
            new_video.channel = channel
            new_video.save()

            for pk in data:
                video = Video.objects.get(pk=pk)
                new_video.final_screens.add(video)

            if playlist_pk:
                playlist = Playlist.objects.get(pk=playlist_pk)
                playlist.videos.add(new_video)

            channel.videos_qty += 1
            channel.save()

            messages.add_message(request, messages.SUCCESS, 'Video publicado con exito')
            return redirect('/channel/@{0}/videos/'.format(request.user.username))
        
        messages.add_message(request, messages.SUCCESS, 'Se presentó un problema con el formulario')
        return redirect('/')



class GetVideosOfChannel(View):
    def get(self, request, *args, **kwargs):
        filter = kwargs['filter']
        user = User.objects.get(username=kwargs['user'])
        channel = Channel.objects.get(user=user)

        context = {}
        match filter:
            case 'latest':
                videos = Video.objects.filter(channel=channel).order_by('-created_at')
                context['videos'] = videos
                return render(request, template_name='pages/channel/components/videos-list.html', context=context)
            case 'popular':
                videos = Video.objects.filter(channel=channel).order_by('-views')
                context['videos'] = videos
                return render(request, template_name='pages/channel/components/videos-list.html', context=context)
            case 'previous':
                videos = Video.objects.filter(channel=channel).order_by('created_at')
                context['videos'] = videos
                return render(request, template_name='pages/channel/components/videos-list.html', context=context)
        
        return HttpResponse('')



class ToggleSuscriber(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        local_channel = Channel.objects.filter(user__username=kwargs['user']).get()
        logged_channel = Channel.objects.get(user=request.user, is_active=True)

        if logged_channel == local_channel:
            messages.add_message(request, messages.ERROR, 'No te puedes suscribir a un canal que te pertenece')
            return redirect('/channel/@{0}/main/'.format(kwargs['user']))

        if not logged_channel in local_channel.suscribers.all():
            local_channel.suscribers.add(logged_channel)
            local_channel.save()
            return redirect('/channel/@{0}/main/'.format(kwargs['user']))

        local_channel.suscribers.remove(logged_channel)
        local_channel.save()
        return redirect('/channel/@{0}/main/'.format(kwargs['user']))

class WatchVideo(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Ok')
        
        
class AddPlaylist(View):
    def get(self, request, *args, **kwargs):
        form = AddPlaylistForm()
        context = {}
        context['form'] = form
        return render(request, template_name='modals/add-playlist.html', context=context)

    def post(self, request, *args, **kwargs):
        channel = Channel.objects.get(user=request.user, is_active=True)          
        form = AddPlaylistForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_playlist = form.save(commit=False)
            new_playlist.channel = channel
            new_playlist.save()

            channel.playlists_qty += 1
            channel.save()

            messages.add_message(request, messages.SUCCESS, 'Playlist publicada con exito')
            return redirect('/channel/@{0}/playlists/'.format(request.user.username))
        
        print(form.errors)
        return HttpResponse(form.errors)
        
        messages.add_message(request, messages.SUCCESS, 'Se presentó un problema con el formulario')
        return redirect('/')


channel_view = ChannelView.as_view()
add_video = AddVideo.as_view()
get_videos_of_channel = GetVideosOfChannel.as_view()
watch_video = WatchVideo.as_view()
toggle_suscriber = ToggleSuscriber.as_view()
add_playlist = AddPlaylist.as_view()
