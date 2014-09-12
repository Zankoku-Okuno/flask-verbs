Flask-Verbs
===========

Nice syntax to help Flask work with HTTP verbs, an important part of a RESTful breakfest.

We're licensed the same as Flask (BSD 3-clause), so no worries.

After installing the extension (`Verbs(app)`), your application will get a new method `verbs`
which works very similarly to the normal `route` method, but it will instead deacorate a whole
class.

All-caps methods on the class will be used to respond to requests of the corresponding method.

```python
@app.verbs('/login')
class Login:
    def __init__(self):
        self.form = LoginForm()

    def GET(self):
        return render_template('login.html', form=self.form)

    def POST(self):
        if self.form.validate():
            # authenticate
            return redirect(url_for('index'))
        else:
            return self.GET()
```

This extension should play nice with others. In particular, you should be able to
use decorators on `.verbs`-enabled classes and on their methods. If you experience
problems, [submit a bug report](https://github.com/Zankoku-Okuno/flask-verbs/issues).
