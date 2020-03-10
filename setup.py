from setuptools import setup

setup(
    name='Flask',
    version='1.0',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.1.1',
        'Flask-Cors>=3.0.8',
        'flask_mysqldb',
        'Flask-SQLAlchemy>=2.4.1',
        'MindsDB==1.13.11'
    ]
)

# cmd to run setup.py
# pip install -e .
