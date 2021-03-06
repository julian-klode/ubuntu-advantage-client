class TxtColor(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    DISABLEGREY = '\033[37m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ACTIVE = 'active'
INACTIVE = 'inactive'
INAPPLICABLE = 'n/a'
ENTITLED = 'entitled'
EXPIRED = 'expired'
NONE = 'none'
COMMUNITY = 'not included'
STANDARD = 'standard'
ADVANCED = 'advanced'

# Colorized status output for terminal
STATUS_COLOR = {
    ACTIVE: TxtColor.OKGREEN + ACTIVE + TxtColor.ENDC,
    INACTIVE: TxtColor.FAIL + INACTIVE + TxtColor.ENDC,
    INAPPLICABLE: TxtColor.DISABLEGREY + INAPPLICABLE + TxtColor.ENDC,
    ENTITLED: TxtColor.OKGREEN + ENTITLED + TxtColor.ENDC,
    EXPIRED: TxtColor.FAIL + EXPIRED + TxtColor.ENDC,
    NONE: TxtColor.DISABLEGREY + NONE + TxtColor.ENDC,
    COMMUNITY: TxtColor.DISABLEGREY + COMMUNITY + TxtColor.ENDC,
    STANDARD: TxtColor.OKGREEN + STANDARD + TxtColor.ENDC,
    ADVANCED: TxtColor.OKGREEN + ADVANCED + TxtColor.ENDC
}

MESSAGE_DISABLED_TMPL = '{title} disabled.'
MESSAGE_NONROOT_USER = 'This command must be run as root (try using sudo)'
MESSAGE_ALREADY_DISABLED_TMPL = '\
{title} is not currently enabled.\nSee `ua status`'
MESSAGE_ENABLED_FAILED_TMPL = 'Could not enable {title}.'
MESSAGE_ENABLED_TMPL = '{title} enabled.'
MESSAGE_ALREADY_ENABLED_TMPL = '{title} is already enabled.\nSee `ua status`'
MESSAGE_INAPPLICABLE_SERIES_TMPL = '\
{title} is not available for Ubuntu {series}.'
MESSAGE_UNENTITLED_TMPL = """\
This subscription is not entitled to {title}.
See `ua status` or https://ubuntu.com/advantage
"""
MESSAGE_UNATTACHED = """\
This machine is not attached to a UA subscription.
See `ua attach` or https://ubuntu.com/advantage
"""

STATUS_TMPL = '{name: <14}{contract_state: <26}{status}'


def format_entitlement_status(entitlement):
    contract_status = entitlement.contract_status()
    operational_status, _details = entitlement.operational_status()
    fmt_args = {
        'name': entitlement.name,
        'contract_state': STATUS_COLOR.get(contract_status, contract_status),
        'status': STATUS_COLOR.get(operational_status, operational_status)}
    return STATUS_TMPL.format(**fmt_args)


def get_upgradeable_esm_package_count():
    import apt_pkg
    apt_pkg.init()

    cache = apt_pkg.Cache(None)
    dependencyCache = apt_pkg.DepCache(cache)
    upgrade_count = 0

    for package in cache.packages:
        if not package.current_ver:
            continue
        upgrades = [v for v in package.version_list if v > package.current_ver]

        for upgrade in upgrades:
            for package_file, _idx in upgrade.file_list:
                if dependencyCache.policy.get_priority(package_file) == -32768:
                    upgrade_count += 1
                    break
    return upgrade_count
