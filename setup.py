# setup.py

from distutils.core import setup

try:
    import py2exe
except ImportError:
    pass

setup(console=["dragon_hunt.py"],
      name="Dragon_Hunt",
      version="3.56",
      description="Dragon Hunt RPG",
      author="Evil Mr Henry",
      author_email="evilmrhenry@emhsoft.net",
      url="http://www.emhsoft.net/dh.html",
      license="GPL",
      py_modules=[], requires=['mock']
)
