from setuptools import setup

setup(name='setup',
      version='0.1.0',
      description='Read the Bible from the terminal with Python and Curses',
      author='rwev',
      author_email='rwev@protonmail.ch',
      url='https://gitlab.com/rwev/bible',
      packages=['bible'],
      include_package_data=True,
      entry_points={
          'console_scripts': ('bible=bible.main:main')
      },      
      install_requires=['PyHyphen'],
      license='GNU GPL 3.0'
      )
