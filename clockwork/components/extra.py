# Bootstrap3 plugin settings
BOOTSTRAP3 = {
    # Set HTML disabled attribute on disabled fields
    'set_disabled': False,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': False,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': 'required',
}

SUMMERNOTE_CONFIG = {
    'iframe': False,
    'width': '100%',
    'height': '200px',
    'disable_upload': True,
}

DATE_EXTENSIONS_OUTPUT_FORMAT_DAY_MONTH_YEAR = "Y-m-d"
DATE_EXTENSIONS_OUTPUT_FORMAT_MONTH_YEAR = "Y-m"
DATE_EXTENSIONS_OUTPUT_FORMAT_YEAR = "Y"

DATE_EXTENSIONS_DATE_INPUT_FORMATS = ("%Y-%m-%d",)
DATE_EXTENSIONS_MONTH_INPUT_FORMATS = ("%Y-%m",)
DATE_EXTENSIONS_YEAR_INPUT_FORMATS = ("%Y",)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M',        # '14:30'
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11212',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Set the cache backend to select2
SELECT2_CACHE_BACKEND = 'select2'