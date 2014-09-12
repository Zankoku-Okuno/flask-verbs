class Verbs:
    """Extend Flask to nicely handle verbs (called methods in HTTP).

    The idea is that a resource (sometimes called endpoint) is mapped to a class,
    and each verb available on that resource is mapped to a method of that class.

    The best way to use this library is to install this extension into your app
    with either `verbs = Verbs(app)` or `verbs = Verbs(); verbs.init_app(app)`.
    There are currently no configuration options.
    
    Installing Verbs extends your `app` with a `verbs` method which acts similarly
    to the `route` method; however, `verbs` decorates an entire class::

        @app.verbs('/accounts/<int:user_id>')
        class Accounts:
            def __init__(self, user_id):
                self.user = User.query.get(user_id) or abort(404)

            def GET(self):
                render_template('user_profile.html', user=self.user)

            @login_required
            def PUT(self):
                # update database
                ...

       Note that while the classes verb-y methods must be all-uppercase, we do not
       artificially limit the verbs available to you: you can even make up custom
       verbs. Conversely, any callable, all-uppercase attribute of the class is
       treated as a valid verb for the resource.

        When the app matches the route to your class, several things happen:

        #. An instance of your class is created, passing arguments from the route
           to the `__init__` method just as `route` passes arguments to its function.
        #. As a convenience, the route arguments are then made attributes of the
           instance. We won't overwrite any already-set attributes (as determined by
           `hasattr`).
        #. The method corresponding to the request verb is called without arguments,
           and its result returned.

        And that's it.  This should mean
        that many other extensions will work naturally with Verbs.
        In particular:

        * The interior of your verb will look very similar to a normal `route`-style
          handler (modulo adding `self.` for parameters),
        * Decorators can be applied onto a verbs-decorated class to affect every method
          for the route,
        * Decorators can be added to the methods of a verbs-decorated class to affect
          just that route+method combination.

        If another flask extension isn't working with this one, submit a bug report at
        https://github.com/Zankoku-Okuno/flask-verbs/issues

        And, when in doubt, the source code is <40 lines, so take a peek.
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from types import MethodType
        app.verbs = MethodType(verbs, app)
        return self

def verbs(app, route, **kwargs):
    def inner(cls):
        # find verb-like methods of the input class
        found_methods = []
        for name, attr in cls.__dict__.items():
            # TODO offer a VERBS_WHITELIST. If a whitelist is present. we'll only check for the listed attrs, but current behavoir is default
            if callable(attr) and name.isupper():
                found_methods.append(name)

        # reconcile the found methods with those passed
        if 'methods' in kwargs:
            assert set(kwargs['methods'] == set(found_methods)), \
                "Verbs decorator: passed HTTP methods do not match HTTP methods of the class."
        else:
            kwargs['methods'] = found_methods

        from flask import request
        # add the appropriate route to the app
        @app.route(route, **kwargs)
        def verb_dispatch(**route_kwargs):
            x = cls(**route_kwargs)
            for k, v in kwargs.items():
                if not hasattr(x, k):
                    setattr(x, k, v)
            return getattr(x, request.method)()

        # no need to return anything other than the original class
        # the point was to update the state of the app's routing tables
        return cls

    return inner