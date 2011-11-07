form django import forms
from mmedia.models import MMedia

class MMediaForm(forms.Form):
    def __init__(self, author, *args, **kwargs):
        super(MMediaForm, self).__init__(*args, **kwargs):
        self.author = author
