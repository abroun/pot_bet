from django.db import models
from djangae import fields

# Create your models here.
class BlogPost( models.Model ):
    title = models.CharField( max_length=100 )
    slug = models.SlugField( max_length=100, unique=True )
    text = models.TextField()
    posted_date = models.DateField( auto_now_add=True )
    author_user_id = models.CharField( max_length=21 )
    
    def __unicode__( self ):
        return self.title
    
    @models.permalink
    def get_absolute_url( self ):
        return ( 'view_blog_post', None, { 'slug': self.slug } )
    
    
    