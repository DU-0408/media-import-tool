from setuptools import setup

setup(
    name="media-import",
    version="1.0",
    py_modules=["media-import"],
    install_requires=[
        "requests",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "media-import=media-import:main"
        ]
    },
)
