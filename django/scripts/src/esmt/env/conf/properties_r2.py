"""
Author: Yogaraja Gopal
This module contains the list of stores, its clients and service details for r2 Stores
"""
import esmt.env.conf.properties as env_prop
CORE_OCTET = '10.34'
SOC_STORES = {
    '10.34.11': ['store', 'testroom', 'dispense', 'dispense1', 'till', 'till1', 'lop'],
    '10.34.13': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.15': ['store', 'testroom1', 'dispense', 'till', 'lop'],
    '10.34.18': ['store', 'testroom', 'dispense13', 'till', 'till1', 'lop'],
    '10.34.33': ['store', 'testroom', 'dispense', 'dispense1', 'till', 'lop56'],
    '10.34.37': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.41': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.51': ['store', 'testroom', 'testroom1', 'dispense', 'dispense1', 'till', 'lop56'],
    '10.34.55': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.57': ['store', 'testroom', 'testroom1', 'dispense', 'dispense1', 'dispense2',
                 'dispense3', 'till', 'lop'],
    '10.34.60': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.68': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.78': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.93': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.95': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.98': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.99': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.102': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.103': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.104': ['store', 'testroom', 'testroom1', 'dispense', 'till', 'lop'],
    '10.34.105': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.108': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.115': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.117': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.118': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.128': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.130': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.131': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.134': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.135': ['store', 'testroom', 'dispense', 'till', 'lop'],
    '10.34.136': ['store', 'testroom', 'dispense', 'till', 'lop']
}

STORE_NUM = env_prop.STORE_NUM

FINAL_OCTET = {
    'dispense13': '13',
    'dispense': '23',
    'dispense1': '24',
    'dispense2': '25',
    'dispense3': '26',
    'till': '35',
    'till1': '36',
    'lop56': '56',

}
FINAL_OCTET.update(env_prop.FINAL_OCTET_BASE)
CLIENT_FINAL_OCTET_MAPPING = {
    '13': 'dispense13',
    '23': 'dispense',
    '24': 'dispense1',
    '25': 'dispense2',
    '26': 'dispense3',
    '35': 'till',
    '36': 'till1',
    '56': 'lop56',
}
CLIENT_FINAL_OCTET_MAPPING.update(env_prop.CLIENT_FINAL_OCTET_MAPPING_BASE)
SERVICE_MAPPING = {
    'lolemail': 'lolemail',
    'crond': 'crond',
    'cups': 'cups',
    'javaqas': 'javaqas',
    'lolsgmb': 'lolsgmb',
    'rsyslog': 'rsyslog',
    'sendmail': 'sendmail',
    'sgmb': 'sgmb',
    'socrates': 'socrates',
    'xmlexportd': 'xmlexportd',
    'iptables': 'iptables',
    'ccApp': 'ccApp',
    'mysqld': 'mysqld',
    'tomcat': 'tomcat',
    'httpd': 'httpd',
    'lanpoller': 'lanpoller',
    'sql32': 'sql32.exe'
}
SERVICES = {
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

STORE_FACTS = {
    "socversion": "/export/socrates/system/jsocver |head -2 | tail -1 | awk '{print $2}'",
    "rhelversion": "cat /etc/redhat-release | awk '{print $7}'",
    "regioncode": "grep Process.DeviceIDs /usr/java/jdk/jre/lib/com.retailJava.javaPOS.properties |"
                  " cut -f2 -d= | awk -F. '{print $3$4}'",
    "storenum": "cat /export/socrates/storenum"
}
