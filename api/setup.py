from setuptools import setup

setup(name='api',
      version='0.1',
      description='API that attaches to Selenium APIs',
      author='Or Rikon',
      author_email='rikonor@gmail.com',
      packages=['api'],
      install_requires=[
          'flask',
          'passlib',
          'bcrypt',
          'mdict',
          'pymongo',
          'nose',
          'enum34'
      ],
      zip_safe=False)
