


def percentageChange(orig, new):
    if isinstance(orig, unicode):
        orig = float(orig)
    if isinstance(new, unicode):
        new = float(new)
    return 100 * (new - orig) / orig