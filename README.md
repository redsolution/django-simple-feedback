# Django feedback application


Open source feedback management system based on the Django framework. You can easily and flexibly embed any feedback form for your site. When the form is submitted you receive an email message containing the form data

## Features
- Easy installation and high level of customization.
- Works through AJAX (without page refresh)
- Flexible configuration of e-mail recipients and email message format.
- Built-in anti-spam protection and easy integration with any additional protection.
- Webpack/gulp compatible.

## Requirements
- Django 1.11.*
- Python 2.7

## Installation and basic usage

1. Install package

    `` pip install git+git://github.com/oldroute/django-simple-feedback.git@1.11``

2. Create (or use) your own application for your feedback forms, for example ``custom_feedback``
3. Configure your setting file:

    - **FEEDBACK_FORMS** - Registry for feedback forms (*required*).
    - **FEEDBACK_FORMS_NAMES** - Registry for feedback form names (*required*).
    - **FEEDBACK_PREFIX_KEY_FIELDS** - Use True if need unique id html element for form fields. Recommended when more than one form (*default: False*).
    - **FEEDBACK_ANTISPAM** - dictionary antispam settings. Include next settings:
        - CHECKING_HIDDEN_FIELD - adding and checking hidden antispam fields in the form (*default: True*)
        - BLOCKING_EXTERNAL_LINKS - checking form content for external links (*default: True*)
    - **FEEDBACK_ADMIN_EXTRA_CLASS** - Admin page customizing: dictionary of extra css classes for fields (*default empty*). For example:
        ``FEEDBACK_ADMIN_EXTRA_CLASS = {'all': 'my-class'}``
    - **FEEDBACK_ADMIN_EXTRA_CSS** - Admin page customizing: dictionary of extra css files for mailing list admin page (*default empty*). For example:
        ``FEEDBACK_ADMIN_EXTRA_CSS = {'all': ['css/admin/common.css']}``

    Simple settings configuration:

    ```python
    # django email settings if they does not exist
    DEFAULT_FROM_EMAIL = 'no-reply@mysite.com'
    MANAGERS = [
        ('websupport', 'websupport+mysite@mycomany.com'),
    ]
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # for local testing

    # feedback settings
    INSTALLED_APPS += ['feedback', '<PROJECT_ROOT>.custom_feedback']
    FEEDBACK_FORMS = {
        'my_form': '<PROJECT_ROOT>.custom_feedback.forms.MyForm',
    }
    FEEDBACK_FORMS_NAMES = {
        'default':  '-- default --',
        'my_form':  'My form name',
    }
    FEEDBACK_PREFIX_KEY_FIELDS = True
    ```

4. Add urlpattern to main urls.py:

    ```python
    urlpatterns = [
        ...
        url(r'^feedback/', include('feedback.urls')),
        ...
    ]
    ```
5. Create your custom form in directory according to FEEDBACK_FORMS settings. For example in dir ``<PROJECT_ROOT>.custom_feedback.forms``
    ```python
    from feedback.forms import BaseFeedbackForm

    class CallForm(BaseFeedbackForm):

        name = forms.CharField()
        email = forms.EmailField()
        phone = forms.CharField()
    ```
6. Call the form in the html template according FEEDBACK_FORMS settings

    ```html
    {% load feedback_tags %}
    ...
    <!--noindex-->
        {% show_feedback 'my_form' %}
    <!--/noindex-->
    ```
    Any feedback form include three states (and accordingly three templates):
    - presentation of form (feedback.html)
    - message after success form sending (thankyou.html)
    - message displayed when spam is blocked (spam.html)

7. Apply migrations and run local server

    ```python
    python manage.py migrate feedback
    python manage.py runserver
    ```

8. Create and configure recipients email adresses and mailing list for your custom form in admin.

    Pay attention to the next mailing list fields:
    - **Form title** - text displayed in form templates as form title.
    - **List of addresses** - customize email recipients list instead of MANAGERS settings.
    - **Default sender email** - customize email sender instead of DEFAULT_FROM_EMAIL settings.
    - **Success message** - text displayed after success form sending.
    - **Message subject** - topic for email message.
    - **Message template** - email message template. All fields of the form are available in the field as variables in brackets. For example:
        ```html
        Name: {{ name }}
        E-mail: {{ email }}
        Phone: {{ phone }}
        ```
**Configure is done!**

## Advansed usage

### Templates structure
To customize any feedback template, stick to the following template structure:
- templates/
    - feedback/
        - my_form/
            - feedback.html
        - feedback.html
        - thankyou.html
        - spam.html
        - field.html

For example, when the "my_form" is rendered, the following priority applies:
1. <PROJECT_ROOT>/templates/feedback/my_form/feedback.html
2. <PROJECT_ROOT>/templates/feedback/feedback.html
3. feedback/templates/feedback/feedback.html # default template from app

The following structure is most userfull:
- templates/
    - feedback/
        - my_form_1/
            - feedback.html # customized form template
        - my_form_2/
            - feedback.html
        - thankyou.html # common templates for all forms
        - spam.html
        - field.html

### Form template
Default form contains javascript from ``{{ form.media }}``. If your customize templates we recomended instead of ``{{ form.media }}`` include script in your base template footer:

```html
<script type="text/javascript" src="/static/feedback/js/feedback.js"></script>
```
Or copy file content in your main.js file

About form customization:

1. To display form fields in the basic order, use default field output.

    **feedback.html**:
    ```html
    {% load feedback_tags %}
    <form>
        ...
        {% for field in form.hidden_fields %}{{ field }}{% endfor %}
        {% for field in form.visible_fields %}
            {% show_field %}
        {% endfor %}
        ...
    </form>

    ```
    In this example, hidden fields are rendered first, and then visible fields are rendered.

2. To separate fields into different groups:

    **forms.py**:
    ```python
    from feedback.forms import BaseFeedbackForm

    class CallForm(BaseFeedbackForm):

        name = forms.CharField(widget=forms.TextInput(attrs={'data-set': 1}))
        email = forms.EmailField(widget=forms.TextInput(attrs={'data-set': 2}))
        phone = forms.CharField(widget=forms.TextInput(attrs={'data-set': 1}))

    ```
    In this example we need to separate fields in two groups: "name" and         "phone" in first group and "email" in second group.

    **feedback.html**:
    ```html
    {% load feedback_tags %}
    <form>
        ...
        {% for field in form.hidden_fields %}{{ field }}{% endfor %}

        <div class="form__row">
            <div class="form__col">
                {% for field in form %}
                    {% show_field field set 1 %}
                {% endfor %}
            </div>
            <div class="form__col">
                {% for field in form %}
                    {% show_field field set 2 %}
                {% endfor %}
            </div>
        </div>
        ...
    </form>

    ```

### Field template

Field rendering is associated with code duplication. To avoid this, use the template tag ``{% show_field %}``.

Tag gets two parameters: "field" and "set" (*optional*). Rendered template get context and two additional varibles
- **atts** - field widget attributes form forms.py
- **input_type** - to separate different fields

**field.html**

```html
<label {{ attrs }} {% if field.errors %}class="error"{% endif %}>
	<span>{{ field.label }}</span>
	{{ field }}
</label>
```
We can combine of ``field.name`` and ``input_type`` to identify any field:

```html
{% if input_type == 'hidden' %}
     {{ field }}
{% elif input_type == 'select' %}
     <div class="{{ attrs.class }}{% if field.errors %} error{% endif %}">
        <label>
            <select required name="{{ field.html_name }}" id="id_{{ field.html_name }}">
              {% for value, name in field.field.choices %}
                    <option {% if field.value|equal:value %}selected{% endif %} value="{{ value }}">{{ name }}</option>
              {% endfor %}
            </select>
            {% if field.label %}<span>{{ field.label }}</span>{% endif %}
        </label>
    </div>
{% elif field.name == 'captcha' %}
	{{ field }}
{% else %}
     <div class="{{ attrs.class }}{% if field.errors %} error{% endif %}">
        <label>
            <span>{{ field.label }}</span>
	    	{{ field }}
        </label>
    </div>
{% endif %}
```
### Additionally
- Administrative interface: to connect the HTML-editor to the "success message" field, install ``django_tinymce`` package (tested for version 2.6.0)

	`` pip install django_tinymce==2.6.0 ``
- If you need additional protection, easy integration with Google reCaptcha v2. Package is available [here](https://github.com/oldroute/django-nocaptcha-recaptcha):

	``pip install git+git://github.com/oldroute/django-nocaptcha-recaptcha.git
``

