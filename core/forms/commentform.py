from django import forms
from core.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Postar sua resposta',
                'oninput': "this.style.height=''; this.style.height=this.scrollHeight + 'px'"
            }),
        }
