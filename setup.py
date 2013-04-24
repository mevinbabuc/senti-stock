from setuptools import setup

setup(name='SentiStock', version='0.2',
      description='Better Stock market recommendation using the Web',
      author='Mevin Babu', 
      author_email='mevinbabuc@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
	  install_requires=['web.py>=0.36', 'Jinja2','nltk','tweetstream',],
     )