from subprocess import call, check_output, DEVNULL
from ipaddress import ip_address


def get_ips_list():
    ips_string = check_output("ipset list truerdp | sed '1,8d'", shell=True, text=True)
    ips_string = ips_string.strip()
    ips_list = ips_string.split(sep='\n')
    return ips_list


def add_ip(ip):
    add_status = call(["ipset", "add", "truerdp", ip], stdout=DEVNULL)
    call(["ipset", "save", "truerdp"], stdout=DEVNULL)
    return add_status


def del_ip(ip):
    del_status = call(["ipset", "del", "truerdp", ip], stdout=DEVNULL)
    call(["ipset", "save", "truerdp"], stdout=DEVNULL)
    return del_status


def ip_format_check(ip):
    try:
        return ip_address(ip.split()[0])
    except ValueError:
        return None
    except IndexError:
        return None
