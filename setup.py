from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='An ELT pipeline that extracts historical daily temperature data for major European cities from Open-Meteo, loads it into DuckDB, and performs SQL-based transformations for climate analysis.',
    author='zzpma',
    license='MIT',
)
