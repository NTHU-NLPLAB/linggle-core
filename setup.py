from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='linggle',
    version='0.1',
    description='Linggle data processing, db, and simple web service.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        # 'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
        'Topic :: Text Processing :: Linguistic',
    ],
    url='https://github.com/NTHU-NLPLAB/Linggle',
    author='NLPLab',
    author_email='jjc@nlplab.cc',
    # license='MIT',
    packages=['linggle'],   
    install_requires=[
        'psycopg2',
        'flask',
        'cassandra-driver'
    ],
    zip_safe=False)
