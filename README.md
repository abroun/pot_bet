
# The PotBET Blog Project

This is a simple blogsite implemented in Django for use on the Google App Engine using [Djangae](https://github.com/potatolondon/djangae)

Markdown rendering is implemented using the [markdown-js](https://github.com/evilstreak/markdown-js) library.


To get started:

 - Clone this repo
 - Run `./install_deps` (this will pip install requirements, and download the App Engine SDK)
 - `python manage.py checksecure --settings=scaffold.settings_live`
 - `python manage.py collectstatic`
 - `python manage.py runserver`

The install_deps helper script will install dependencies into a 'sitepackages' folder which is added to the path. Each time you run it your
sitepackages will be wiped out and reinstalled with pip. The SDK will only be downloaded the first time (as it's a large download).

## Deployment

Assuming that you have access to the pot-bet Google App, run

    $ appcfg.py update ./

If you have two-factor authentication enabled in your Google account, run:

    $ appcfg.py --oauth2 update ./

