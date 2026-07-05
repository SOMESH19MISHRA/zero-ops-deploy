from setuptools import setup, find_packages

setup(
    name="zero-ops-deploy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "zero-ops-deploy=zero_ops_deploy.cli:init",
        ],
    },
)
