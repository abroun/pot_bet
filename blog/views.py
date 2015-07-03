from blog.models import BlogPost
from blog.forms import BlogPostForm
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
import utils
import djangae.db.transaction
import markdown
import bleach

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

NUM_SNIPPET_LINES = 3
NUM_ITEMS_PER_PAGE = 5

#---------------------------------------------------------------------------------------------------
# Tag and attribute whitelists for when converting user entered markdown to sanitized HTML
ALLOWED_HTML_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "h1", "h2", "h3", "h4",
    "h5", "h6", "hr", "i", "img", "li", "ol", "p", "pre", "strong", "table", "tr", "td", "ul"
]

ALLOWED_HTML_ATTRIBUTES = {
    "a" : [ "href", "title" ], 
    "abbr" : [ "title" ], 
    "acronym": [ "title" ],
    "img" : [ "src", "alt" ]
}

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
def format_text( markdown_text ):
    
    """Converts markdown text to sanitized HTML"""
    
    return bleach.clean( markdown.markdown( markdown_text ), 
        tags=ALLOWED_HTML_TAGS, attributes=ALLOWED_HTML_ATTRIBUTES )

#---------------------------------------------------------------------------------------------------
def get_formatted_snippet( markdown_text ):
    
    # Get the first NUM_SNIPPET_LINES of non blank text in the markdown
    lines = markdown_text.split( "\n" )
    
    snippet_lines = []
    num_non_blank_lines = 0
    
    for line in lines:
        
        snippet_lines.append( line )
        
        if line.strip() != "":
            num_non_blank_lines += 1
            
            if num_non_blank_lines >= NUM_SNIPPET_LINES:
                break   # Found enough lines
            
    # Now format the snippet text
    snippet_text = "\n".join( snippet_lines )
    return format_text( snippet_text )

#---------------------------------------------------------------------------------------------------
def index( request ):
    
    # Work out which page we should show
    page = request.GET.get( "page", 0 )
    if page != None:
        try:
            page = int( page )
            if page < 0:
                page = 0

        except:
            page = 0    # Ignore any parse errors and set page to a safe value
    
    start_index = page*NUM_ITEMS_PER_PAGE
    
    all_posts = BlogPost.objects.all().order_by( "-posted_date_time" )
    num_posts = len( all_posts )
    num_pages = int( num_posts/NUM_ITEMS_PER_PAGE ) + 1
    if num_posts > 0 and num_posts%NUM_ITEMS_PER_PAGE == 0:
        num_pages -= 1
    
    templateDict = get_template_dict( "Home", request.user )
    templateDict[ "page" ] = page
    templateDict[ "num_pages" ] = num_pages
    templateDict[ "posts" ] = all_posts[ start_index:start_index+5 ]
    
    for post in templateDict[ "posts" ]:
        post.formatted_snippet = get_formatted_snippet( post.text )
    
    return render_to_response( "blog/index.html", templateDict )

#---------------------------------------------------------------------------------------------------
def view_post( request, slug ):   

    templateDict = get_template_dict( "Home", request.user )
    templateDict[ "post" ] = get_object_or_404( BlogPost, slug=slug )
    templateDict[ "post_formatted_text" ] = format_text( templateDict[ "post" ].text )
    
    return render_to_response( "blog/view_post.html", templateDict )

#---------------------------------------------------------------------------------------------------
def admin_view_post( request, slug ):   

    if not utils.user_has_admin_rights( request.user ):
        raise PermissionDenied

    templateDict = get_template_dict( "Home", request.user )
    templateDict[ "post" ] = get_object_or_404( BlogPost, slug=slug )
    templateDict[ "post_formatted_text" ] = format_text( templateDict[ "post" ].text )
    
    return render_to_response( "blog/admin_view_post.html", templateDict )
    
#---------------------------------------------------------------------------------------------------
def edit_post( request, slug ):   

    if not utils.user_has_admin_rights( request.user ):
        raise PermissionDenied

    blog_post = get_object_or_404( BlogPost, slug=slug )
    
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = BlogPostForm( request.POST, instance=blog_post )

        if form.is_valid():
            
            form.save()
            
            # Go back to the admin page
            return redirect( "blog.views.admin" )

    else:
        # Create a form from the existing blog post
        form = BlogPostForm( instance=blog_post )

    templateDict = get_template_dict( "Admin", request.user )
    templateDict[ "form" ] = form
    templateDict[ "editing_post" ] = True
    templateDict[ "edit_link" ] = blog_post.get_absolute_edit_url()

    return render( request, "blog/add_edit_post.html", templateDict )

#---------------------------------------------------------------------------------------------------
def delete_post( request, slug ):   

    if not utils.user_has_admin_rights( request.user ):
        raise PermissionDenied

    get_object_or_404( BlogPost, slug=slug ).delete()
    
    return redirect( "blog.views.admin" )
    
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
            if unicode( post._get_pk_val() ) == pk:
                pkFound = True
                break
            
        if not pkFound:
            blogPost = BlogPost.objects.get( pk=pk )
            if blogPost != None:
                blogPosts.append( blogPost )
    
    
    blogPosts = sorted( blogPosts, reverse=True,
        key=lambda x: x.posted_date_time if x.posted_date_time != None else timezone.now() )
    
    # Mark all blog posts which the current user owns
    for post in blogPosts:
        if unicode( post.author_user_id ) == request.user.username:
            post.cur_user_is_owner = True
        else:
            post.cur_user_is_owner = False
    
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
            
            newPost = form.save( commit=False )
            newPost.author_user_id = request.user.username
            newPost.author_email = request.user.email
            newPost.save()
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

    return render( request, "blog/add_edit_post.html", templateDict )
    
#---------------------------------------------------------------------------------------------------
def permission_denied( request ):
    
    return render_to_response( "blog/403.html", get_template_dict( "Admin", request.user ) )