from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class SharePostForm(forms.Form):
    title = forms.CharField(max_length=25)
    comment = forms.CharField(required=False, widget=forms.Textarea)
    # email = forms.EmailField()
    destination = forms.EmailField()

