from setuptools import setup

setup(
    name="scm_gui",
    version="0.1.0",
    packages=["src"],
    entry_points={
        "console_scripts": [
            "scm_gui = src.__main__:main",
        ]
    }
)
