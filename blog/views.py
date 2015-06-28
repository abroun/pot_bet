from blog.models import BlogPost
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
import utils

from google.appengine.api import users

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
def get_template_dict( activePageName, user ):
    
    templateDict = {
        "pageList" : PAGE_LIST,
        "activePageName" : activePageName,
        "loggedIn" : user.is_authenticated()
    }
    
    if templateDict[ "loggedIn" ]:
        templateDict[ "logoutLink" ] = users.create_logout_url( "/" )
    
    return templateDict

#---------------------------------------------------------------------------------------------------
def index( request ):
    
    templateDict = get_template_dict( "Home", request.user )
    templateDict[ "posts" ] = BlogPost.objects.all()[:5]
    
    return render_to_response( "blog/index.html", templateDict )

#---------------------------------------------------------------------------------------------------
def view_post( request, slug ):   

    templateDict = get_template_dict( None, request.user )
    templateDict[ "post" ] = get_object_or_404( BlogPost, slug=slug )

    return render_to_response( "blog/view_post.html", templateDict )
    
#---------------------------------------------------------------------------------------------------
def admin( request ):
    
    if not utils.user_has_admin_rights( request.user ):
        raise PermissionDenied
    
    return render_to_response( "blog/admin.html", get_template_dict( "Admin", request.user ) )
    
#---------------------------------------------------------------------------------------------------
def permission_denied( request ):
    
    return render_to_response( "blog/403.html", get_template_dict( "Admin", request.user ) )