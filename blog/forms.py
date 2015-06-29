from django.forms import ModelForm
from blog.models import BlogPost

#---------------------------------------------------------------------------------------------------
class BlogPostForm( ModelForm ):

    class Meta:
        model = BlogPost
        fields = [ "title", "slug", "text", "tags" ]

