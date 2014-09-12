from distutils.core import setup

setup(
    name='Flask-Verbs',
    version='0.1.0',
    author='Zankoku Okuno',
    author_email='zankoku.okuno@gmail.com',
    packages=['flask.ext'],
    url='https://github.com/Zankoku-Okuno/flask-verbs',
    license='LICENSE',
    description='Extend Flask with nice syntax for working with HTTP methods (a special case of REST verbs)',
    long_description=open('README.md').read(),
    install_requires=[
        "Flask >= 0.10.0", #FIXME this probably works with lower versions of flask
    ],
)
