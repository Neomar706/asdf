from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from .forms import AddPlaylistForm, EditPlaylistForm
from .models import Playlist
from apps.channel.models import Video
from apps.channel.models import Channel, Video
from urllib.parse import unquote
from json import loads as load_json
from datetime import timedelta
from apps.channel.views import suscription
from django.conf import settings
from .utils import avg_image_color

import os


class AddPlaylist(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = AddPlaylistForm()
        context = {}
        context['form'] = form
        context['action'] = 'create'
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
        
        
        messages.add_message(request, messages.ERROR, 'Se presentó un problema con el formulario')
        return redirect('/')
        

class AddVideosToPlaylist(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.filter(channel__user=request.user).all().order_by('-created_at')
        playlist = Playlist.objects.get(pk=kwargs['playlist'])
        playlist_videos = playlist.videos.all()

        videos_list = []
        list_pks = []
        for video in videos:
            video_obj = {}
            video_obj['pk']          = video.pk
            video_obj['title']       = video.title
            video_obj['thumbnail']   = video.thumbnail
            video_obj['duration']    = video.duration
            video_obj['views_qty']   = video.views.count()
            video_obj['created_at']  = video.created_at
            video_obj['in_playlist'] = 'true' if video in playlist_videos else 'false'
            videos_list.append(video_obj)
            if video in playlist_videos:
                list_pks.append(video.pk)

        context = {}
        context['videos'] = videos_list
        context['list_pks'] = list_pks
        context['playlist_pk'] = kwargs['playlist']
        return render(request, template_name='modals/add-videos-to-playlist.html', context=context)
    
    def post(self, request, *args, **kwargs):
        encode_uri  = request.POST['encodeuri']
        decode_uri  = unquote(encode_uri)
        data        = load_json(decode_uri)
        playlist_pk = kwargs['playlist']

        playlist = Playlist.objects.get(pk=playlist_pk)
        playlist_videos = playlist.videos.all()
        playlist_duration = playlist.duration \
            if playlist.duration is not None \
            else timedelta(seconds=0)

        videos_added = False
        videos_added_count = 0
        for pk in data:
            video = Video.objects.get(pk=pk)
            if not video in playlist_videos:
                playlist_duration += video.duration
                playlist.videos.add(video)
                videos_added = True
                videos_added_count += 1

        videos_removed = False
        videos_removed_count = 0
        for video in playlist_videos:
            if not video.pk in data:
                playlist_duration -= video.duration
                playlist.videos.remove(video)
                videos_removed = True
                videos_removed_count += 1

        if videos_added or videos_removed:
            playlist.duration = playlist_duration
            playlist.updated_at = timezone.now()
            playlist.save()

            message = 'Lista actualizada con exito: ({0}) videos añadidos ({1}) removidos'
            message = message.format(videos_added_count, videos_removed_count)
            messages.add_message(request, messages.SUCCESS, message)
            
        return redirect('/channel/@{0}/playlists'.format(request.user.username))


class EditPlaylist(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EditPlaylistForm()
        context = {}
        context['form'] = form
        context['action'] = 'edit'
        context['playlist_pk'] = kwargs['playlist']
        return render(request, template_name='modals/add-playlist.html', context=context)

    def post(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk=kwargs['playlist'])
        form = EditPlaylistForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            playlist.title        = data['title']        or playlist.title
            playlist.thumbnail    = data['thumbnail']    or playlist.thumbnail
            playlist.description  = data['description']  or playlist.description
            playlist.is_published = data['is_published'] or playlist.is_published
            playlist.save()

            messages.add_message(request, messages.SUCCESS, 'Playlist editada con exito')
            return redirect('/channel/@{0}/playlists/'.format(request.user.username))
        
        messages.add_message(request, messages.ERROR, 'Se presentó un problema con el formulario')
        return redirect('/')
    

class RemovePlaylist(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk=kwargs['playlist'])
        context = {}
        context['playlist'] = playlist
        return render(request, template_name='modals/remove-playlist.html', context=context)

    def post(self, request, *args, **kwargs):
        channel = Channel.objects.get(user=request.user)
        playlist = get_object_or_404(Playlist, pk=kwargs['playlist'])

        playlist.delete()
        channel.playlists_qty -= 1
        channel.save()

        messages.add_message(request, messages.SUCCESS, 'Playlist eliminada con exito')
        return redirect('/channel/@{0}/playlists/'.format(request.user.username))



class PlaylistView(View):
    def get(self, request, *args, **kwargs):
        playlist = Playlist.objects.filter(channel__user=request.user, channel__is_active=True, title='WL')[0]
        path = os.path.join(settings.BASE_DIR, 'media', *str(playlist.videos.all()[0].thumbnail).split('/'))
        
        context = {}
        context['playlist'] = playlist

        bigcard = {}
        bigcard['title']      = 'Ver más tarde'
        bigcard['video']      = playlist.videos.all()[0]
        bigcard['bgcolor']    = avg_image_color(path)
        bigcard['videos_qty'] = playlist.videos.count()
        bigcard['updated_at'] = playlist.updated_at

        context['bigcard'] = bigcard

        print("bigcard['video'].pk: ", bigcard['video'].pk)

        suscription(request, context)
        return render(request, template_name='pages/playlist/index.html', context=context)


class AddToPlaylist(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(pk=kwargs['pk'])
        playlist = Playlist.objects.filter(channel__user=request.user, channel__is_active=True, title='WL')[0]
        playlist.videos.add(video)
        return redirect(request.POST['path'])

add_playlist = AddPlaylist.as_view()
add_videos_to_playlist = AddVideosToPlaylist.as_view()
edit_playlist = EditPlaylist.as_view()
remove_playlist = RemovePlaylist.as_view()
playlist_view = PlaylistView.as_view()
add_to_playlist = AddToPlaylist.as_view()