from blog.models import BlogPost
from blog.forms import BlogPostForm
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import utils
import djangae.db.transaction

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
    
    # As we're using the GAE datastore objects.all() may not return consistent results
    # especially if a post has just been added. Having an optional primary key parameter
    # allows us to enforce strong consistency by performing a get for that object
    pk = request.GET.get( "pk", None )
    blogPosts = list( BlogPost.objects.all() )
    
    if pk != None:
        pkFound = False
        for post in blogPosts:
            if post._get_pk_val() == pk:
                pkFound = True
                break
            
        if not pkFound:
            blogPost = BlogPost.objects.get( pk=pk )
            if blogPost != None:
                blogPosts.append( blogPost )
    
    templateDict = get_template_dict( "Admin", request.user )
    templateDict[ "posts" ] = blogPosts
    
    return render_to_response( "blog/admin.html", templateDict )

#---------------------------------------------------------------------------------------------------
def add_post( request ):
    
    if not utils.user_has_admin_rights( request.user ):
        raise PermissionDenied
    
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = BlogPostForm( request.POST )

        if form.is_valid():
            
            newPost = form.save()
            pk = newPost._get_pk_val()
            
            # Go back to the admin page, but pas back the primary key of the 
            # new object so that we can find it
            response = redirect( "blog.views.admin" )
            response[ "Location" ] += ( "?pk=" + str( pk ) )
            return response

    else:
        # Create a blank form
        form = BlogPostForm()

    templateDict = get_template_dict( "Admin", request.user )
    templateDict[ "form" ] = form

    return render( request, "blog/add_post.html", templateDict )
    
#---------------------------------------------------------------------------------------------------
def permission_denied( request ):
    
    return render_to_response( "blog/403.html", get_template_dict( "Admin", request.user ) )