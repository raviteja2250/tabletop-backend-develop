""" Utilization function for interacting with time """


def minutes_between(time1, time2):
    """ Calculate minute between 2 times """
    time_delta = (time2 - time1)
    total_seconds = time_delta.total_seconds()

    result = total_seconds / 60
    if result < 0:
        return -result

    return result
