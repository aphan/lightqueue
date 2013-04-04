from distutils.core import setup

setup(
    name='lightqueue',
    version='0.1.0',
    author='Adam Phan',
    author_email='aphansh@gmail.com',
    packages=['lightqueue', 'lightqueue.test'],
    scripts=['bin/start_lightqueue.py'],
    url='https://github.com/aphan/lightqueue',
    license='MIT',
    description='lightweight Python job queue with multiprocessing support',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'lightqueue = lightqueue.commandline:start',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    install_requires=[
        "redis >= 2.7.2",
    ],
)
