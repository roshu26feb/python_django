"""
Author: Yogaraja Gopal
This module contains the list of Solar7 details
"""
SOLAR7_ENV = {
    '10.34.250.90': {
        'name': 'solar7-sok',
        'desc': 'Solar7 SOK',
        'services': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    },
    '10.34.250.115': {
        'name': 'solar7-sok-db',
        'desc': 'Solar7 SOK DB',
        'services': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    },
    '10.38.0.171': {
        'name': 'solar7-fin',
        'desc': 'Solar7 Finland',
        'services': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    },
    '10.38.0.110': {
        'name': 'solar7-aus',
        'desc': 'Solar7 AUS',
        'services': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    }
}
