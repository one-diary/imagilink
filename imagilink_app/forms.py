from django import forms
from .models import Links

class LinkForm(forms.ModelForm):
    target_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "text-input form-control form-control-md", "placeholder": "Paste here the target url..."}))

    seo_title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "text-input form-control form-control-md", "placeholder": "please keep title short..."}))

    # description = forms.CharField(widget=forms.TextInput(
    #     attrs={"class": "sim-input", "placeholder": "Description here..."}))

    custom_url = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control text-input", "placeholder": "custom name (optional)"}))

    seo_description = forms.CharField(widget=forms.Textarea(
        attrs={"class": "text-input form-control form-control-md", "placeholder": "Description here...", "cols":30, "rows":5}))
    
    seo_image = forms.CharField(widget=forms.HiddenInput())

    author = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Links
        fields = ('target_url','seo_title','custom_url', 'seo_description', 'seo_image', 'author',)