from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="pyncddns",
    version="1.0",
    description="python namecheap dyn-dns updater",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/pyncddns",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],
    keywords="namecheap ddns dyn-dns updater",
    packages=find_packages(),
    install_requires=[
        "requests", "loguru", "pyrunnable"
    ],
    entry_points={
        'console_scripts': [
            'pyncddns = pyncddns.__main__:main'
        ]
    },
    long_description_content_type="text/markdown",
)
