from django import forms
from core.models import *


class Add_Prodect_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            'id':"fname",
            'name':"fname"}),
        self.fields['product_category'].widget.attrs.update({
            'type':"Select",
            'class':"form-control"
            }),
        self.fields['price'].widget.attrs.update({
            'type':"NumberInput",
            'class':"form-control"
            }),
        self.fields['product_quantity'].widget.attrs.update({
            'type':"NumberInput",
            'class':"form-control"
            }),
        self.fields['product_image'].widget.attrs.update({
            'type':"FileInput",
            'class':"form-control"
            }),
        self.fields['description'].widget.attrs.update({
            'type':"TextArea",
            'class':"form-control"
            })
    class Meta:
        model=Product
        fields=['product_name','product_category','price','description','product_quantity','product_image']
class Add_Image_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photos'].widget.attrs.update({
            'type':"FileInput",
            'class':"form-control",
            'multiple':'True',
            })
    class Meta:
        model=Image
        fields=['photos']

    

class Check_out_Form(forms.ModelForm):
    class Meta:
        model=Check_out_model
        fields=['country','first_name','last_name','company_name','address','state','post_code','order_note']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({
            'type':"Select",
            'required':"",
            'class':"form-control",
            'id':"c_country",
            'name':"c_country"}),
        self.fields['first_name'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            }),
        self.fields['last_name'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            }),
        self.fields['company_name'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            }),
        self.fields['address'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            'cols':"30",
            'rows':"7" 
            }),
        self.fields['state'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            }),
        self.fields['post_code'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            }),
        self.fields['order_note'].widget.attrs.update({
            'type':"text",
            'class':"form-control",
            'cols':"30",
            'rows':"5" 
            }),



        
