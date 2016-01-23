from setuptools import setup

from pylibrets import __version__

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'pylibrets',
      version = __version__,
      description = 'RETS client library',
      long_description = readme(),
      author = 'Fernando Herrera',
      author_email = 'wkdglitch@gmail.com',
      url = 'http://github.com/wkdglitch/pylibrets',
      keywords = 'rets librets',
      license = 'MIT',
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
      packages = ['pylibrets'],
      install_requires = [
          'requests',
      ],
      include_package_data = True,
      zip_safe = False)