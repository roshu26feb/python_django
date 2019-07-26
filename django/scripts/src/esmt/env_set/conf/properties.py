"""
Author: Yogaraja Gopal
This is a property file which holds all the configurations regarding the environment
"""
RUNDECK_URL = 'http://rundeck.uk.specsavers.com/api/'
AUTH_TOKEN = '5aWkFYm1LGSfxMU29PaRGXYVE7kymi8K'
RUNDECK_JOB_ID = {
    'status': 'ed34cadf-b033-40f7-aeea-cbbf878af35d',
    'start_stop': 'b5e40748-ae96-433a-b745-d81338ea4336',
    'interface_status': '91fd8f64-29df-44ac-9ed5-2a018241dc4b'
}

ENV = {
    'soc-uk': {
        '10.34.29': ['store', 'testroom', 'dispense1', 'till', 'lop']
    },
    'soc-nl': {
        '10.34.108': ['store', 'testroom', 'dispense', 'till', 'lop']
    },
    'soc-roi': {
        '10.34.117': ['store', 'testroom', 'dispense', 'till', 'lop']
    },
    'soc-esp': {
        '10.34.13': ['store', 'testroom', 'dispense', 'till', 'lop']
    },
    'soc-fin': {
        '10.34.69': ['store', 'testroom', 'dispense', 'till']
    },
    'plato-leg': {
        '10.2.166.25': ['server']
    },
    'plato-aus': {
        '10.80.3.30': ['server']
    },
    'plato-fin': {
        '10.34.0.241': ['server']
    },
    'aristotle': {
        '10.34.49': ['activemq']
    },
    'solar7-sok': {
        '10.34.250.109': ['server']
    },
    'solar7-aus': {
        '10.34.250.111': ['server']
    },
    'solar7-fin': {
        '10.34.250.113': ['server']
    }
}
ENV_DESCRIPTION = {
    '10.34.29': 'Socrates UK R3',
    '10.34.108': 'Socrates NL R2',
    '10.34.117': 'Socrates ROI R2',
    '10.34.13': 'Socrates ESP R2',
    '10.34.69': 'Socrates Fin',
    '10.2.166.25': 'Legacy Plato',
    '10.80.3.30': 'Plato 7 (Aus)',
    '10.34.0.241': 'Plato 7 (Fin)',
    '10.34.250.109': 'Solar 7(Lab) <br> SOK',
    '10.34.250.111': 'Solar 7(Hub) <br> Aus',
    '10.34.250.113': 'Solar 7(Hub) <br> Fin'
}
STORE_NUM = {
    '10.34.29': '8013',
    '10.34.108': '8021',
    '10.34.18': '0913',
    '10.34.117': '2959',
    '10.34.13': '9922'
}
soc_r2_clients = {
    '1': 'store',
    '80': 'testroom',
    '13': 'dispense13', '23': 'dispense', '24': 'dispense1',
    '35': 'till', '36': 'till1',
    '56': 'lop56', '69': 'lop'
}
CLIENT_FINAL_OCTET_MAPPING = {
    'soc-uk': {
        '1': 'store',
        '80': 'testroom',
        '13': 'dispense', '14': 'dispense1',
        '50': 'till',
        '69': 'lop'
    },
    'soc-nl': soc_r2_clients,
    'soc-roi': soc_r2_clients,
    'soc-esp': soc_r2_clients,
    'soc-fin': {
        '1': 'store',
        '80': 'testroom',
        '13': 'dispense',
        '50': 'till'
    },
    'plato-leg': {'25': 'server'},
    'plato-aus': {'30': 'server'},
    'plato-fin': {'241': 'server'},
    'aristotle': {'202': 'activemq'},
    'solar7-sok': {'109': 'server'},
    'solar7-aus': {'111': 'server'},
    'solar7-fin': {'113': 'server'}

}
soc_r2_ip_mapping = {
    'store': '1',
    'testroom': '80', 'testroom1': '81', 'testroom2': '82', 'testroom3': '83',
    'testroom4': '84', 'testroom5': '85',
    'dispense13': '13', 'dispense': '23', 'dispense1': '24', 'dispense2': '25',
    'till': '35', 'till1': '36',
    'lop56': '56', 'lop': '69',
}
CLIENT_IP_MAPPING = {
    'soc-uk': {
        'store': '1',
        'testroom': '80', 'testroom1': '81', 'testroom2': '82', 'testroom3': '83',
        'testroom4': '84', 'testroom5': '85',
        'dispense': '13', 'dispense1': '14', 'dispense2': '15', 'dispense3': '16',
        'till': '50', 'till1': '51',
        'lop': '69',
    },
    'soc-nl': soc_r2_ip_mapping,
    'soc-roi': soc_r2_ip_mapping,
    'soc-esp': soc_r2_ip_mapping,
    'soc-fin': {
        'store': '1',
        'testroom': '80',
        'dispense': '13',
        'till': '50'
    },
    'plato-leg': {'server': '25'},
    'plato-aus': {'server': '30'},
    'plato-fin': {'server': '241'},
    'aristotle': {'activemq': '202'},
    'solar7-sok': {'server': '109'},
    'solar7-aus': {'server': '111'},
    'solar7-fin': {'server': '113'}
}

soc_r2 = {
    'store': ['lolemail', 'crond', 'cups', 'javaqas', 'lolsgmb', 'rsyslog', 'sendmail', 'sgmb',
              'socrates', 'xmlexportd', 'iptables', 'ccApp'],
    'testroom': ['tomcat'],
    'testroom1': ['tomcat'],
    'testroom2': ['tomcat'],
    'testroom3': ['tomcat'],
    'testroom4': ['tomcat'],
    'testroom5': ['tomcat'],
    'dispense': ['mysqld', 'httpd'],
    'dispense13': ['mysqld', 'httpd'],
    'dispense1': ['mysqld', 'httpd'],
    'dispense2': ['mysqld', 'httpd'],
    'dispense3': ['mysqld', 'httpd'],
    'till': ['sql32', 'lanpoller'],
    'till1': ['sql32', 'lanpoller'],
    'lop56': ['lolemail', 'lolsgmb', 'sgmb'],
    'lop': ['lolemail', 'lolsgmb', 'sgmb']
}
ENV_SERVICE_LIST = {
    'soc-uk': {
        'store': ['httpd', 'rj_to_soa_bridge', 'progress_to_rj_bridge', 'backoffice', 'tomcat6',
                  'mysqld', 'lolsgmb', 'ntpd', 'specseodd', 'xmlexport', 'sgmb', 'ccApp'],
        'testroom': ['backoffice'],
        'dispense': ['backoffice'],
        'dispense1': ['backoffice'],
        'till': ['backoffice', 'mysqld'],
        'lop': ['mysql', 'tomcat6', 'vnc']
    },
    'soc-nl': soc_r2,
    'soc-roi': soc_r2,
    'soc-esp': soc_r2,
    'soc-fin': {
        'store': ['socratesBroker', 'socratesContainer', 'rj_to_soa_bridge', 'backoffice',
                  'specseodd', 'mysqld', 'vsftpd'],
        'testroom': ['backoffice', 'mysql'],
        'dispense': ['backoffice', 'mysql'],
        'till': ['backoffice', 'mysqld']
    },
    'plato-leg': {
        'server': ['legacyPlatoBroker', 'legacyPlatoContainer', 'mysql']
    },
    'plato-aus': {
        'server': ['platoContainer', 'platoBroker', 'vsftpd', 'mysqld']
    },
    'plato-fin': {
        'server': ['jboss-fuse', 'platoContainer', 'plato-broker', 'vsftpd', 'mysqld',
                   'smx4-plato']
    },
    'aristotle': {
        'activemq': ['transitionComponentContainer', 'aristotleContainer', 'aristotleBroker']
    },
    'solar7-aus': {
        'server': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    },
    'solar7-fin': {
        'server': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    },
    'solar7-sok': {
        'server': ['mmlabsBroker', 'labsBroker', 'tomcat6', 'mysql', 'cups']
    }
}
SERVICE_NAME_MAPPING = {
    'progress_to_rj_bridge': 'progress_to_rj_bridge',
    'rj_to_soa_bridge': 'rj_to_soa_bridge',
    'backoffice': 'backoffice',
    'tomcat6': 'tomcat6',
    'httpd': 'httpd',
    'mysqld': 'mysqld',
    'lolsgmb': 'lolsgmb',
    'ntpd': 'ntpd',
    'specseodd': 'specseodd',
    'xmlexport': 'xmlexport',
    'sgmb': 'sgmb',
    'ccApp': 'ccApp',
    'lolemail': 'lolemail',
    'crond': 'crond',
    'cups': 'cups',
    'javaqas': 'javaqas',
    'rsyslog': 'rsyslog',
    'sendmail': 'sendmail',
    'socrates': 'socrates',
    'xmlexportd': 'xmlexportd',
    'iptables': 'iptables',
    'mysql': 'mysql',
    'vnc': 'winvnc4',
    'sql32': 'sql32.exe',
    'lanpoller': 'lanpoller',
    'progress-db': 'progress',
    'transitionComponentContainer': 'transitionComponentContainer',
    'aristotleContainer': 'aristotleContainer',
    'aristotleBroker': 'aristotleBroker',
    'socratesBroker': 'socratesBroker',
    'socratesContainer': 'socratesContainer',
    'vsftpd': 'vsftpd',
    'jboss-fuse': 'jboss-fuse',
    'platoContainer': 'platoContainer',
    'plato-broker': 'plato-broker',
    'smx4-plato': 'smx4-plato',
    'legacyPlatoBroker': 'legacyPlatoBroker',
    'legacyPlatoContainer': 'legacyPlatoContainer',
    'platoBroker': 'platoBroker',
    'labsBroker': 'labsBroker',
    'mmlabsBroker': 'mmlabsBroker'
}
PING_ENV_LIST = {
    'soc-uk-store': '10.34.29.1',
    'soc-uk-testroom': '10.34.29.80',
    'soc-uk-dispense': '10.34.29.13',
    'soc-uk-dispense1': '10.34.29.14',
    'soc-uk-till': '10.34.29.50',
    'soc-uk-lop': '10.34.29.69',
    'soc-nl-store': '10.34.108.1',
    'soc-nl-testroom': '10.34.108.80',
    'soc-nl-dispense': '10.34.108.23',
    'soc-nl-dispense1': '10.34.108.24',
    'soc-nl-till': '10.34.108.35',
    'soc-nl-lop': '10.34.108.69',
    'soc-roi-store': '10.34.117.1',
    'soc-roi-testroom': '10.34.117.80',
    'soc-roi-dispense': '10.34.117.23',
    'soc-roi-till': '10.34.117.35',
    'soc-roi-lop': '10.34.117.69',
    'soc-esp-store': '10.34.13.1',
    'soc-esp-testroom': '10.34.13.80',
    'soc-esp-dispense': '10.34.13.23',
    'soc-esp-till': '10.34.13.35',
    'soc-esp-lop': '10.34.13.69',
    'soc-fin-store': '10.34.69.1',
    'soc-fin-testroom': '10.34.69.80',
    'soc-fin-dispense': '10.34.69.13',
    'soc-fin-till': '10.34.69.50',
    'soc-170-store': '10.84.170.1',
    'plato-aus': '10.80.3.30',
    'plato-fin': '10.34.0.241',
    'plato-leg': '10.2.166.25',
    'aristotle': '10.34.49.202',
    'solar7-sok': '10.34.250.109',
    'solar7-aus': '10.34.250.111',
    'solar7-fin': '10.34.250.113',
    'on-premise-soa-a': '10.75.8.92:22',
    'on-premise-soa-a-admin': '10.75.8.92:7001',
    'on-premise-soa-a-managed': '10.75.8.92:8001',
    'adf-managed-server': '10.75.8.92:8005',
    'on-premise-odi': '10.75.8.88:22',
    'on-premise-odi-admin': '10.75.8.88:7005',
    'on-premise-odi-server': '10.75.8.88:8001',
    'azure-soa-a': '10.243.96.12',
    'azure-soa-a-admin': '10.243.96.12:7001',
    'azure-soa-a-server': '10.243.96.12:8001',
    'azure-soa-a-wsm': '10.243.96.12:8002',
    'azure-soa-d': '10.243.96.5',
    'azure-soa-d-admin': '10.243.96.5:7001',
    'azure-soa-d-server': '10.243.96.5:8001',
    'azure-soa-d-wsm': '10.243.96.5:8002',
    'azure-odi': '10.243.96.10',
    'azure-odi-admin': '10.243.96.10:7001',
    'azure-odi-server': '10.243.96.10:8001',
    'azure-odi-wsm': '10.243.96.10:8002',
    'azure-mft': '10.243.32.26',
    'azure-mft-admin': '10.243.32.26:7001',
    'azure-mft-server': '10.243.32.26:8001',
    'azure-mft-wsm': '10.243.32.26:8002',
    'ebs': '10.243.96.4',
    'azure-ebs-http': '10.243.96.4:8000',
    'azure-ebs-weblogic': '10.243.96.4:7002',
    'azure-osb': '10.243.96.7',
    'azure-osb-admin': '10.243.96.7:7001',
    'azure-osb-server': '10.243.96.7:8001',
    'azure-osb-wsm': '10.243.96.7:8002',
    'edw': '10.75.8.125',
    'nordics-ebs': '10.75.8.150',
    'vcp': '10.243.96.14:22',
    'azure-vcp-http': '10.243.96.14:8000',
    'azure-vcp-weblogic': '10.243.96.14:7002',
    'jda-wms': '10.248.88.4:22'
}
INTERFACE_LIST = {
    'plato-leg': {'10.2.166.25': ['ftp']},
    'soc-uk': {'10.34.29.1': ['vsftpd']},
    'soc-roi': {'10.34.117.1': ['vsftpd']},
    'soc-nl': {'10.34.108.1': ['vsftpd']},
    'soc-esp': {'10.34.13.1': ['vsftpd']},
    'aristotle': {'10.34.49.202': ['transitionComponentContainer', 'aristotleContainer',
                                   'aristotleBroker']}
}

soc_r2 = {
    'store': ['lolemail', 'crond', 'cups', 'javaqas', 'lolsgmb', 'rsyslog', 'sendmail', 'sgmb',
              'socrates', 'xmlexportd', 'iptables', 'ccApp'],
    'testroom': ['tomcat'],
    'testroom1': ['tomcat'],
    'testroom2': ['tomcat'],
    'testroom3': ['tomcat'],
    'testroom4': ['tomcat'],
    'testroom5': ['tomcat'],
    'dispense': ['mysqld', 'httpd'],
    'dispense13': ['mysqld', 'httpd'],
    'dispense1': ['mysqld', 'httpd'],
    'dispense2': ['mysqld', 'httpd'],
    'dispense3': ['mysqld', 'httpd'],
    'till': ['sql32', 'lanpoller'],
    'till1': ['sql32', 'lanpoller'],
    'lop56': ['lolemail', 'lolsgmb', 'sgmb'],
    'lop': ['lolemail', 'lolsgmb', 'sgmb']
}

