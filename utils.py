import cProfile, pstats, io

def time_and_slow_calls(function):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        s = io.StringIO()

        retval = function(*args, **kwargs)

        pr.disable()
        s = io.StringIO()
        sortby = 'tottime'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(10)
        print(s.getvalue())

        return retval

    return wrapper
