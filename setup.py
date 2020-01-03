from setuptools import setup, find_packages

setup(
    name="tikzmagic",
    version="1.1.0dev",

    packages=find_packages(),
    install_requires=['IPython','wand'],

    description='''
        A Jupyter extension for compiling and displaying images described by the TikZ language.
        Fork of https://github.com/robjstan/tikzmagic
        ''',
    url='https://github.com/xblahoud/tikzmagic',

    author='Fanda Blahoudek',
    author_email='fandikb+devel@gmail.com',

    license='MIT',
    classifiers=['Programming Language :: Python :: 3.5'],
)
