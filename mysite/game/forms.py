from django import forms
from .models import  Game, Genre_list

class GameCreateForm(forms.ModelForm):
    genre_choice = forms.ModelMultipleChoiceField(queryset=Genre_list.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Game
        fields = ['title', 'genre_choice', 'developer', 'release_at', 'info', 'thumbnail', 'video']

    def save(self, commit=True):
        game = self.instance
        genre_list = '/'.join([qs.genre_list for qs in self.cleaned_data['genre_choice']])
        game.genre = genre_list
        game.save()
        return game