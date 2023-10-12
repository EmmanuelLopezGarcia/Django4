from django import forms

# The EmailPostForm inherits from the base Form class.

class EmailPostForm(forms.Form):

    name = forms.CharField(max_length=50)

    email = forms.EmailField()

    to = forms.EmailField()

    # comments is not required by setting it as False and has a custom widget to render the field.
    # Using widgets you can modify the default rendered field so the HTML element can be different

    comments = forms.CharField(required=False, widget=forms.Textarea)

    