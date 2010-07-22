MENU_PROXY_RULES += [
    {
        'name': 'feedback',
        'method': 'insert',
        'proxy': 'menuproxy.proxies.ReverseProxy',
        'viewname': 'feedback_page',
        'title_text': gettext_noop('Feedback'),
    }, ]
