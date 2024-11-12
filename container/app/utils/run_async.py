from threading import Thread


def run_method_async(method_name, *args, **kwargs):
    """Run a method asynchronously."""
    Thread(target=method_name, args=args, kwargs=kwargs).start()
