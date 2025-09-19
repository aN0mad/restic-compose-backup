"""
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * command to execute
#
# Supports special characters: * , - /
# Does not support: @yearly, @monthly, @weekly, @daily, @hourly, @reboot
"""
QUOTE_CHARS = ['"', "'"]


def generate_crontab(config):
    """Generate a crontab entry for running backup job"""
    command = config.cron_command.strip()
    schedule = config.cron_schedule

    if schedule:
        schedule = schedule.strip()
        schedule = strip_quotes(schedule)
        if not validate_schedule(schedule):
            schedule = config.default_crontab_schedule
    else:
        schedule = config.default_crontab_schedule

    return f'{schedule} {command}\n'


def validate_schedule(schedule: str):
    """Validate crontab format with support for / , - modifiers"""
    parts = schedule.split()
    if len(parts) != 5:
        return False

    validators = [
        (0, 59),   # Minute
        (0, 23),   # Hour
        (1, 31),   # Day of month
        (1, 12),   # Month
        (0, 6),    # Day of week
    ]

    for part, (min_val, max_val) in zip(parts, validators):
        if not validate_field(part, min_val, max_val):
            return False

    return True


def validate_field(field: str, min_val: int, max_val: int):
    """Validate a crontab field string with modifiers like *, -, /, ,"""
    # Split on commas first: e.g. 1,5,10-15/2
    for segment in field.split(','):
        if segment == '*':
            continue
        # Handle step values: */5 or 1-10/2
        if '/' in segment:
            base, step = segment.split('/')
            if not step.isdigit() or int(step) <= 0:
                return False
        else:
            base = segment

        if base == '*':
            continue
        elif '-' in base:
            start, end = base.split('-')
            if not (start.isdigit() and end.isdigit()):
                return False
            start, end = int(start), int(end)
            if not (min_val <= start <= end <= max_val):
                return False
        elif base.isdigit():
            val = int(base)
            if not (min_val <= val <= max_val):
                return False
        else:
            return False

    return True


def strip_quotes(value: str):
    """Strip enclosing single or double quotes if present"""
    if value and value[0] in QUOTE_CHARS:
        value = value[1:]
    if value and value[-1] in QUOTE_CHARS:
        value = value[:-1]
    return value
