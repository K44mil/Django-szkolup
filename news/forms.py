from django import forms
from tinymce import TinyMCE
from .models import Post


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
            widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'thumbnail', 'overview', 'content', 'featured']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Tytuł"
        self.fields['thumbnail'].label = "Miniaturka"
        self.fields['overview'].label = "Opis"
        self.fields['content'].label = "Treść"
        self.fields['featured'].label = "Umieść na stronie głównej"

