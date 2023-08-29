from django import forms
from .models import Role, Candidate, VoteTable, VoteCheck

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role']
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['candidate_name', 'display_image', 'role']
        widgets = {
            'candidate_name': forms.Select(attrs={'class': 'form-control'}),
            'display_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Select(attrs={'class': 'form-control'}),
        }

class VoteTableForm(forms.ModelForm):
    class Meta:
        model = VoteTable
        fields = ['voted_by', 'role_name', 'candidates']
        widgets = {
            'voted_by': forms.Select(attrs={'class': 'form-control'}),
            'role_name': forms.Select(attrs={'class': 'form-control'}),
            'candidates': forms.Select(attrs={'class': 'form-control'}),
        }

class VoteCheckForm(forms.ModelForm):
    class Meta:
        model = VoteCheck
        fields = ['voters', 'role']
        widgets = {
            'voters': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
