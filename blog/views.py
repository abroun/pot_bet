from blog.models import BlogPost
from django.shortcuts import render_to_response, get_object_or_404

def index( request ):
    
    if request.user.is_authenticated():
        print ">>>>>>> User is authenticated"
    else:
        print ">>>>>>> User is NOT authenticated"
    
    return render_to_response( 'blog/index.html', {
        'posts' : BlogPost.objects.all()[:5]
    })

def view_post( request, slug ):   
    return render_to_response( 'blog/view_post.html', {
        'post' : get_object_or_404( BlogPost, slug=slug )
    })