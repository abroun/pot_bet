from django.db import models
from djangae import fields
from django.core.urlresolvers import reverse

# Create your models here.
class BlogPost( models.Model ):
    title = models.CharField( max_length=100 )
    slug = models.SlugField( max_length=100, unique=True )
    text = models.TextField()
    posted_date_time = models.DateTimeField( auto_now_add=True )
    author_user_id = models.CharField( max_length=21 )
    author_email = models.EmailField()
    
    def __unicode__( self ):
        return self.title
    
    def get_absolute_url( self ):
        return reverse( "view_blog_post", kwargs={ "slug": self.slug } )
    
    def get_absolute_admin_view_url( self ):
        return reverse( "admin_view_blog_post", kwargs={ "slug": self.slug } )
    
    def get_absolute_edit_url( self ):
        return reverse( "edit_blog_post", kwargs={ "slug": self.slug } )
    
    def get_absolute_delete_url( self ):
        return reverse( "delete_blog_post", kwargs={ "slug": self.slug } )
    
    