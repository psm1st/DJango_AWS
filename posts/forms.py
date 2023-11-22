from django import forms

from .models import Post
class PostBasedForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class PostCreateForm(forms.ModelForm):
    class Meta(PostBasedForm.Meta):
        fields = ['image','content']

class PostUpdateForm(PostBasedForm):
    class Meta(PostBasedForm.Meta):
        fields = ['image','content']

class PostDetailForm(PostBasedForm):
    def __init__(self,*args,**kwargs):
        super(PostDetailForm,self).__init__(*args,**kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['disabled'] = True