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
        'numpy>=1.18.0',
        'pandas>=0.25.3',
        'scikit-learn>=0.22',
        'scipy>=1.4.1',
        'flask_mysqldb',
    ]
)

# cmd to run setup.py
# pip install -e .
