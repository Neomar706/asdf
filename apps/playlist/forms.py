from django import forms
from .models import Playlist


class AddPlaylistForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'placeholder:font-medium focus:px-5 px-5 pb-3 bg-[#181818] outline-none border-cgray-800 focus:border-none focus:outline-none text-white w-full rounded-md',
            'placeholder': 'Título',
            'tabindex': '1',
            'autofocus': 'true'
        }),
        required=True
    )
    thumbnail = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'hidden'
        }),
        label='Imagen de miniatura',
        required=True,
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'placeholder:font-medium focus:px-5 px-5 pb-3 bg-[#181818] outline-none border-cgray-800 focus:border-none focus:outline-none text-white w-full rounded-md tracking-wide h-64 resize-none',
            'placeholder': 'Descripción (opcional)',
            'tabindex': '3',
        }),
        required=False
    )
    is_published = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'hidden',
            'checked': 'true'
        }),
        required=False,
    )
    class Meta:
        model = Playlist
        fields = ['title',
                  'thumbnail',
                  'description',
                  'is_published']
        

class EditPlaylistForm(AddPlaylistForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'placeholder:font-medium focus:px-5 px-5 pb-3 bg-[#181818] outline-none border-cgray-800 focus:border-none focus:outline-none text-white w-full rounded-md',
            'placeholder': 'Título',
            'tabindex': '1',
            'autofocus': 'true'
        }),
        required=False
    )
    thumbnail = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'hidden'
        }),
        label='Imagen de miniatura',
        required=False,
    )