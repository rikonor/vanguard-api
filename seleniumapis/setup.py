from setuptools import setup

setup(name='seleniumapis',
      version='0.1',
      description='Query Vanguard and other sites using the Selenium API',
      author='Or Rikon',
      author_email='rikonor@gmail.com',
      packages=['vanguard'],
      install_requires=[
          'selenium',
          'nose'
      ],
      zip_safe=False)
