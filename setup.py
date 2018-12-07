import setuptools


setuptools.setup(
    name='handout',
    version='0.3.0',
    description='Add Markdown text and inline figures to your Python script.',
    url='http://github.com/danijar/handout',
    install_requires=[],
    packages=['handout'],
    package_data={'handout': ['data/*']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'License :: OSI Approved :: Apache Software License',
    ],
)
