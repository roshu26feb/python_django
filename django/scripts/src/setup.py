"""
This module contains the setup details for packaging
"""
from setuptools import setup, find_packages

setup(
    name='esmt',
    version='0.2.73',
    description='Environment Services Management Tool',
    author='Yogaraja Gopal, Pradnya Puranik, Bharat Rathod',
    author_email='yogaraja.gopal@specsavers.com, pradyna.puranik@specsavers.com, bharatp.rathod@specsavers.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=['manage.py', 'esmt.ini', 'esmt.sh'],
    python_requires='>=3',
    install_requires=["Django==1.11.3",
                      "djangorestframework==3.6.3",
                      "django-bootstrap3==9.0.0",
                      "django-datetime-widget",
                      "requests>=2.18.1",
                      "django-templates-macros",
                      "python-crontab",
                      "mysqlclient",
                      "pbr",
                      "python-jenkins",
                      "uwsgi",
                      "pyyaml",
                      "ruamel.yaml==0.15.94"],
    extras_require={
        "test": [
            "colorama>=0.3.3",
            "coverage>=4.0.3",
            "django-nose>=1.4.2",
            "nose>=1.3.7",
            "pinocchio>=0.4.2"
        ]
    },
)
