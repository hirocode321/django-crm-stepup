from django import forms
from .models import Customer, Tag

class CustomerForm(forms.ModelForm):
    """
    # タグを複数選択可能なフィールドに明示的に指定
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="タグ"
    )
    """

    class Meta:
        model = Customer
        fields = ['company_name', 'contact_name', 'email', 'phone', 'tags']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: ○○株式会社'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 山田太郎'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '090-0000-0000'}),
            'tags': forms.CheckboxSelectMultiple(),  # 明示的に指定
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # タグを名前でソート
        self.fields['tags'].queryset = Tag.objects.all().order_by('name')

# 商談履歴フォーム
from .models import Activity
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_date', 'status', 'note']
        widgets = {
            'activity_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }