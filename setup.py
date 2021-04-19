from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='pycayennelpp',
    version='2.2.0',
    python_requires='>=3.6',
    description='Encoder and Decoder for CayenneLLP',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='cayenne lpp iot lora lorawan ttn',
    url='http://github.com/smlng/pycayennelpp',
    author='smlng',
    author_email='s@mlng.net',
    license='MIT',
    packages=['cayennelpp'],
    setup_requires=["pytest-runner"],
    tests_require=['pytest'],
    include_package_data=True
)
