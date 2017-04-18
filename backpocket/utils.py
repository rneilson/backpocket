import datetime, uuid


# UUID v4 validation
def validuuid(uid, version=4):
    '''Ensures given uid argument is a valid UUID (default version 4)
    Returns UUID instance if valid, None if not.
    Can be a UUID instance, or any type which uuid.UUID() accepts as input.
    '''

    if isinstance(uid, uuid.UUID):
        # Easiest case, uid is already UUID
        # (UUID constructor chokes on UUID instances,
        # so we have to explicitly check)
        return uid
    else:
        # Attempt conversion, return if successful
        try:
            # Insist on version
            retuid = uuid.UUID(uid, version=version)
        except ValueError as e:
            # Invalid, return None instead of raising exception
            retuid = None

        return retuid


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


# Datetime string conversion
# Uses same format as Django internal, except without subsecond resolution
# DATETIMEFMT = '%Y-%m-%dT%H:%M:%SZ'
# DATEONLYFMT = '%Y-%m-%d'
# DATEFULLFMT = '%Y-%m-%dT%H:%M:%S.%fZ'
