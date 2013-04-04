import sys


class Func(object):

    def __init__(self, func, args, kwargs, job):
        self.args = args
        self.kwargs = kwargs
        self.job = job

        try:
            # If the function passed is an instance method, set who called the
            # function, the function itself, and the function args
            self.caller = func.__self__
            self.name = func.__name__
        except AttributeError:
            # Function passed isn't an instance method
            self.func = func

    def execute(self):
        try:
            # If the function is an instance method, it will have the caller
            # set so we have to bind the method
            func = getattr(self.caller, self.name)
        except AttributeError:
            func = self.func

        try:
            # Execute the func then tell parent job that this func finished
            # successfully or if it failed
            func(*self.args, **self.kwargs)
            self.job.finished_successfully()
        except (KeyboardInterrupt, SystemExit):
            # The worker will automatically handle adding this func's job
            # back onto the queue
            sys.exit()
        except:
            # Some exception ocurred that caused the job to fail
            self.job.failed(sys.exc_info()[0])

    def __repr__(self):
        # Return the class of the caller, the name of the function, and the
        # args and kwargs
        # import ipdb; ipdb.set_trace()

        args_str = ','.join(str(i) for i in self.args)
        kwargs_str = ','.join(key + '=' + repr(self.kwargs[key]) for key
                              in self.kwargs)

        full_args_str = '(' + args_str
        if len(kwargs_str) > 0:
            full_args_str += ', ' + kwargs_str
        full_args_str += ')'

        try:
            return (self.caller.__class__.__name__ + ': ' + self.name +
                    full_args_str)
        except AttributeError:
            return self.func.__name__ + full_args_str
