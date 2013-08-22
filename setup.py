from setuptools import setup, find_packages

long_description = '\n\n'.join([open('README.md').read()
                                ])


setup(
    name='vagrantboxes',
    version='%%version%%',
    description='vagrantboxes is a wrapper around www.vagrantbox.es allowing people to simplify the local installation of boxes listed there.',
    long_description=long_description,
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Environment :: Console",
        'Intended Audience :: Developers',
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities'
    ],
    keywords='vagrant boxes installation',
    py_modules=['vagrantboxes'],
    author='David Loureiro',
    author_email='david.loureiro1@gmail.com',
    url='https://github.com/dloureiro/vagrantboxes',
    license='GNU AGPL v3',
    install_requires=[
        'setuptools',
        'lxml'
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    [console_scripts]
    vagrantboxes = vagrantboxes:main
    """,
)
