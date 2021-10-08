from django import forms
from . models import Item , Sub_category
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class ItemModelForm(forms.ModelForm): #form for Item addition

    class Meta:
        model=Item
        fields=('name','category', 'sub_category','price','image','un')
        # widgets = {
        #     'category' : forms.Select(attrs={'class' : 'form-control'}),
        # }
    
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args,**kwargs)
        self.fields['un'].initial = self.request.user.id
        self.fields['un'].widget = forms.HiddenInput()
        self.fields['sub_category'].queryset = Sub_category.objects.all()

        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = Sub_category.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.sub_category_set.order_by('name')



class SignUpForm(UserCreationForm):   #Form for signup for user registration
    # email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    # password1 = forms.CharField(widget=forms.PasswordInput,help_text="Min 8 characters,should contain special charecters , alphabets and Numbers ")
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )