from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pycayennelpp',
      version='0.2',
      description='Encoder and Decoder for CayenneLLP',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
      ],
      keywords='cayenne lpp iot lora lorawan ttn',
      url='http://github.com/smlng/pycayennelpp',
      author='smlng',
      author_email='s@mlng.net',
      license='MIT',
      packages=['cayennelpp'],
      include_package_data=True,
      zip_safe=False)
