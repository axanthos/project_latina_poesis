from setuptools import setup

setup(
    name="Latina_Poesis",
    packages = ["Textableprototype"],
    entry_points = {"orange.widgets": ("Textable Proto = Textableprototype")},
    )

##python setup.py develop