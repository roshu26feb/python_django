import os
from esmt.settings.base import INSTALLED_APPS

# Installed Apps
INSTALLED_APPS += ('django_nose', )
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_OUTPUT_DIR = os.environ.get('TEST_OUTPUT_DIR', '.')
NOSE_ARGS = [
    '--verbosity=2',                  # verbose output
    '--nologcapture',                 # don't output log capture
    '--with-coverage',                # activate coverage report
    '--cover-package=delivery_db',           # coverage reports will apply to these packages
    '--with-spec',                    # spec style tests
    '--spec-color',
    '--with-xunit',                   # enable xunit plugin
    '--xunit-file=%s/unittests.xml' % TEST_OUTPUT_DIR,
    '--cover-xml',                    # produce XML coverage info
    '--cover-xml-file=%s/coverage.xml' % TEST_OUTPUT_DIR,
]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': 'esmt_unit_test'
        }
    }
}
