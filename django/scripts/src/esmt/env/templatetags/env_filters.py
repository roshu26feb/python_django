"""
Author: Yogaraja Gopal
This module contains the Template tags for env App
"""
import re
from django import template
from esmt.env.conf.properties import FINAL_OCTET
from esmt.env.conf.properties_r2 import FINAL_OCTET as R2_FINAL_OCTET
register = template.Library()


@register.filter(name="sort_list")
def sort_list(values):
    """
    This template tag is used to  sort list
    """
    return sorted(values)


@register.filter(name="dict_val")
def dict_val(values, arg):
    """
    This template tag is used to return dictionary value
    """
    if arg in values:
        return values[arg]
    return ""


@register.filter(name="dict_items")
def dict_items(values):
    """
    This template tag is used to return dictionary items
    """
    return values.items()


def check_status(line, text):
    """
    This template tag is used to return the status
    """
    search_run = re.search(r"" + text, line, re.I)
    return search_run


@register.filter(name="repl_status")
def repl_status(value):
    """
    This template tag is used to check the rep_log and return css_class
    """
    soc_log = (value['soc_log'] if 'soc_log' in value else "")
    plato_log = (value['plato_log'] if 'plato_log' in value else "")

    if check_status(soc_log, "Completed OK") and check_status(plato_log, "Completed OK"):
        return "btn-success"
    elif check_status(soc_log, "Failed") or check_status(plato_log, "Failed"):
        return "btn-danger"
    return "btn-warning"


@register.filter(name='mount_sts')
def mount_sts(mnt_detail):
    """
    This template tag is used to check the mount details and return the css_class
    """
    sts = "btn-success"
    if mnt_detail != '':
        mount_data = mnt_detail["mount"]
        if mount_data:
            for mounts in mount_data:
                mnt = mounts[4].split("%")
                mnt_per = int(mnt[0])
                if mnt_per >= 95:
                    sts = 'btn-danger'
                elif 89 < mnt_per < 95:
                    sts = ('btn-warning' if sts != 'btn-danger' else sts)
                else:
                    sts = ('btn-success' if sts != 'btn-danger' and sts != 'btn-warning' else sts)
        else:
            sts = 'btn-danger'
    else:
        sts = 'btn-danger'
    return sts


@register.filter(name='region_name')
def region_name(region_code):
    """
    This template tag returns the region name based on region code
    """
    region_code_name = {
        '020304': 'UK',
        '020321': 'scottish',
        '020322': 'Nothern Ireland',
        '020323': 'Guernsey & Jersey',
        '1315': 'Spain',
        '0218': 'ROI',
        '0708': 'NL'
    }
    return region_code_name[region_code]


@register.filter(name='split2')
def split2(value):
    """
    This template tag is used to split the values
    """
    return value.split(".")[2]


@register.simple_tag(name='clientIp')
def clientIp(store, client, *args):
    """
    This template tag forms the ip Address and returns it base don the client name
    """
    r2_r3 = args[0]
    if r2_r3 == "R3":
        return "10.34." + store + "." + FINAL_OCTET[client]
    elif r2_r3 == "R2":
        return "10.34." + store + "." + R2_FINAL_OCTET[client]
    return "Invalid region supplied"
