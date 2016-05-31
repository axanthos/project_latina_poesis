from setuptools import setup

setup(
    name="OWLatinText",
    packages = ["MyLatinText"],
    entry_points = {"orange.widgets": ("OWLatinText = MyLatinText")},
    )

##python setup.py develop