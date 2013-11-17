from setuptools import setup


setup(
    name='siphon',
    version='0.5.0',
    author='Brian Cline',
    author_email='brian.cline@gmail.com',
    description='A somewhat intelligent remote-to-local '
                'file transfer utility.',
    long_description=open('README.md').read(),
    license='MIT',
    keywords='remote file transfer sync copy',
    url='https://github.com/briancline/siphon',
    packages=['siphon'],
    install_requires=['sqlite3', 'paramiko'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Archiving :: Mirroring',
    ],
)
