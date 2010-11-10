# ---- feedback ----

INSTALLED_APPS += ['feedback']

{% if 'redsolutioncms.django-menu-proxy' in cms_settings.installed_packages %}
try:
    MENU_PROXY_RULES
except NameError:
    MENU_PROXY_RULES = []

MENU_PROXY_RULES += [
    {
        'name': 'feedback',
        'method': 'insert',
        'proxy': 'menuproxy.proxies.ReverseProxy',
        'viewname': 'feedback_page',
        'title_text': gettext_noop('Feedback'),
    },
]
{% endif %}
