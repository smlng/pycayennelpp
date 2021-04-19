from setuptools import setup
import sdist_upip


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='micropython-pycayennelpp',
    version='2.2.0',
    description='Encoder and Decoder for CayenneLLP',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: MicroPython'
    ],
    keywords='cayenne lpp iot lora lorawan ttn',
    url='http://github.com/smlng/pycayennelpp',
    author='smlng',
    author_email='s@mlng.net',
    license='MIT',
    packages=['cayennelpp'],
    cmdclass={'sdist': sdist_upip.sdist},
    include_package_data=True
)
