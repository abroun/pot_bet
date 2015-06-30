from django.forms import ModelForm, TextInput, Textarea
from blog.models import BlogPost

#---------------------------------------------------------------------------------------------------
class BlogPostForm( ModelForm ):

    class Meta:
        model = BlogPost
        fields = [ "title", "slug", "text", "tags" ]
        widgets = {
            "title" : TextInput( attrs={ "class" : "form-control" } ),
            "slug" : TextInput( attrs={ "class" : "form-control" } ),
            "text" : Textarea( attrs={ "class" : "form-control" } ),
            "tags" : TextInput( attrs={ "class" : "form-control" } )
        }
