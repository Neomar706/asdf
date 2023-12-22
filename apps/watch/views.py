from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount
from apps.channel.models import Channel, Video
from apps.channel.views import suscription
from .models import Comment
from apps.history.models import History


class WatchVideo(View):
    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=kwargs['pk'])
        related_videos = Video.objects \
            .filter(Q(channel=video.channel) | Q(title__icontains=video.title)) \
            .exclude(pk=video.pk)
        comments = Comment.objects.filter(video=video).all()

        context = {}
        context['video'] = video
        context['related_videos'] = related_videos
        context['comments'] = comments

        suscription(request, context, video.channel)

        if request.user.is_authenticated:
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            channel_logged = Channel.objects.get(user=request.user, is_active=True)
            history = History.objects.filter(channel=channel_logged)

            if not channel_logged in video.views.all():
                video.views.add(channel_logged)

            video_in_history = False
            for his in history:
                if his.video == video:
                    video_in_history = True

            if not channel_logged.is_paused_history and not video_in_history:
                History.objects.create(channel=channel_logged, video=video)

            context['channel']    = channel_logged
            context['avatar_url'] = social_account.get_avatar_url()

        return render(request, template_name='pages/watch/index.html', context=context)



class ToggleLike(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(pk=kwargs['video'])
        channel_logged = Channel.objects.get(user=request.user, is_active=True)
        clicked_btn = request.POST['clicked']

        if clicked_btn == 'like':
            if channel_logged in video.dislikes.all():
                video.dislikes.remove(channel_logged)
            if channel_logged in video.likes.all():
                video.likes.remove(channel_logged)
            else:
                video.likes.add(channel_logged)

        elif clicked_btn == 'dislike':
            if channel_logged in video.likes.all():
                video.likes.remove(channel_logged)
            if channel_logged in video.dislikes.all():
                video.dislikes.remove(channel_logged)
            else:
                video.dislikes.add(channel_logged)

        return redirect(request.POST['path'])



class CreateComment(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video_pk = kwargs['video']
        issuer_channel_pk = kwargs['issuer_channel']

        comment = request.POST['comment']

        if not comment:
            return redirect('/watch/{0}/'.format(video_pk))

        video = Video.objects.get(pk=video_pk)
        issuer_channel = Channel.objects.get(pk=issuer_channel_pk)

        Comment.objects.create(channel=issuer_channel,
                               video=video,
                               content=comment)

        messages.add_message(request, messages.SUCCESS, 'Se añadió tu comentario')
        return redirect('/watch/{0}/'.format(video_pk))



class ToggleLikeComment(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['comment'])
        channel_logged = Channel.objects.get(user=request.user, is_active=True)
        clicked_btn = request.POST['clicked']

        if clicked_btn == 'like':
            if channel_logged in comment.dislikes.all():
                comment.dislikes.remove(channel_logged)
            if channel_logged in comment.likes.all():
                comment.likes.remove(channel_logged)
            else:
                comment.likes.add(channel_logged)

        elif clicked_btn == 'dislike':
            if channel_logged in comment.likes.all():
                comment.likes.remove(channel_logged)
            if channel_logged in comment.dislikes.all():
                comment.dislikes.remove(channel_logged)
            else:
                comment.dislikes.add(channel_logged)

        return redirect(request.POST['path'])


watch_video = WatchVideo.as_view()
toggle_like = ToggleLike.as_view()
create_comment = CreateComment.as_view()
toggle_like_comment = ToggleLikeComment.as_view()