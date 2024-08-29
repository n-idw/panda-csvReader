import io
import os.path as op

from setuptools import setup

here = op.abspath(op.dirname(__file__))

# Get the long description from the README file
with io.open(op.join(here, 'README.md'), mode='rt', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='panda-csvReader',
    version='1',
    description='CSV reader for PANDA STT hit and truth data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/n-idw/panda-csvReader',
    packages=['trackml'],
    install_requires=[
        'numpy',
        'pandas>=0.21.0',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
