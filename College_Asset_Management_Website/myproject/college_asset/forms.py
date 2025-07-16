# classroom_asset/forms.py
from django import forms
from .models import RegisteredAsset, Classroom, ClassroomAsset

class RegisteredAssetForm(forms.ModelForm):
    class Meta:
        model = RegisteredAsset
        fields = ['asset_name']

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['classroom_no', 'classroom_name', 'division']

class ClassroomAssetForm(forms.ModelForm):
    asset = forms.ModelChoiceField(queryset=RegisteredAsset.objects.all())
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())

    class Meta:
        model = ClassroomAsset
        fields = ['classroom', 'asset', 'quantity', 'inactive_quantity']