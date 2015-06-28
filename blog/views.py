from blog.models import BlogPost
from django.shortcuts import render_to_response, get_object_or_404

#---------------------------------------------------------------------------------------------------
class PageInfo:
    """Helper class which holds the name of an important page along with a link
       to the page"""
    
    def __init__( self, name, link ):
        self.name = name
        self.link = link

PAGE_LIST = [
    PageInfo( "Home", "/" ),
    PageInfo( "Admin", "/admin" )
]

#---------------------------------------------------------------------------------------------------
def index( request ):
    
    if request.user.is_authenticated():
        print ">>>>>>> User is authenticated"
    else:
        print ">>>>>>> User is NOT authenticated"
    
    return render_to_response( 'blog/index.html', {
        "pageList" : PAGE_LIST,
        "activePageName" : "Home",
        "posts" : BlogPost.objects.all()[:5]
    })

#---------------------------------------------------------------------------------------------------
def view_post( request, slug ):   
    return render_to_response( "blog/view_post.html", {
        "pageList" : PAGE_LIST,
        "activePageName" : None,
        "post" : get_object_or_404( BlogPost, slug=slug )
    })