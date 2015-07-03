from scaffold.settings import *

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000 #30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True


SECURE_REDIRECT_EXEMPT = [
    # App Engine doesn't use HTTPS internally, so the /_ah/.* URLs need to be exempt.
    # djangosecure compares these to request.path.lstrip("/"), hence the lack of preceding /
    r"^_ah/"
]

SECURE_CHECKS += ["scaffold.checks.check_csp_sources_not_unsafe"]

# CSP settings for production (DEBUG=False) mode.
CSP_DEFAULT_SRC = copy.copy( DEFAULT_CSP_DEFAULT_SRC )
CSP_STYLE_SRC = copy.copy( DEFAULT_CSP_STYLE_SRC )
CSP_FONT_SRC = copy.copy( DEFAULT_CSP_FONT_SRC )
CSP_FRAME_SRC = copy.copy( DEFAULT_CSP_FRAME_SRC )
CSP_SCRIPT_SRC = copy.copy( DEFAULT_CSP_SCRIPT_SRC )
CSP_IMG_SRC = copy.copy( DEFAULT_CSP_IMG_SRC )
CSP_CONNECT_SRC = copy.copy( DEFAULT_CSP_CONNECT_SRC )

DEBUG = False
TEMPLATE_DEBUG = False
