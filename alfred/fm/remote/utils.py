import urllib.request


def get_ip(ipv4=True):
    """
    Returns the Public IP address of the current machine.

    :param ipv4: If True, returns the IPv4 address. If False, returns the IPv6 address.
    :type ipv4: bool
    :return: The Public IP address of the current machine.
    :rtype: str
    """
    prefix = 'v4' if ipv4 else 'v6'
    external_ip = urllib.request.urlopen(
        f"https://{prefix}.ident.me").read().decode('utf8')
    return external_ip.strip()
