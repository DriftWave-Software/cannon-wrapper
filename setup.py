import os
import re
import sys
import platform
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from pathlib import Path

# Get version from __init__.py
with open('__init__.py', 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.1.0'  # Default version if not found


# A CMakeExtension class to handle CMake build
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


# Command to build the extension using CMake
class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the extension")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        
        # Required for Windows
        if platform.system() == "Windows":
            cmake_args = [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}']
            
            # Determine architecture and set appropriate EDSDK path
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
                # Use 64-bit EDSDK
                edsdk_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', 'EDSDK_64')
            else:
                # Use 32-bit EDSDK
                edsdk_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', 'EDSDK')
                
            # Add EDSDK path to CMake arguments
            cmake_args += [f'-DEDSDK_PATH={edsdk_path}']
        else:
            cmake_args = [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}']
            # Add lib/EDSDK path for non-Windows platforms
            edsdk_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', 'EDSDK')
            cmake_args += [f'-DEDSDK_PATH={edsdk_path}']

        # Set build type
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        # Configure platform-specific build options
        if platform.system() == "Windows":
            cmake_args += [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}']
            build_args += ['--', '/m']
        else:
            cmake_args += [f'-DCMAKE_BUILD_TYPE={cfg}']
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = f'{env.get("CXXFLAGS", "")} -DVERSION_INFO=\\"{self.distribution.get_version()}\\"'
        
        # Build directory
        build_dir = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        # Run CMake
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=build_dir, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=build_dir)


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cannon_wrapper',
    version=version,
    author='Canon EDSDK Team',
    author_email='info@example.com',
    description='Python wrapper for Canon EDSDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/username/cannon_wrapper',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    ext_modules=[CMakeExtension('edsdk_bindings')],
    cmdclass={'build_ext': CMakeBuild},
    install_requires=[
        'numpy',  # For image data handling
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'mypy',
            'black',
        ],
    },
    include_package_data=True,
    package_data={
        'cannon_wrapper': ['py.typed'],
    },
    zip_safe=False,
) 