@echo off
echo ==========================================
echo Building Canon EDSDK Python Bindings
echo ==========================================

:: Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Please make sure Python is installed and in your PATH.
    exit /b 1
)

:: Install required dependencies first with pip
echo Installing required dependencies...
pip install wheel setuptools cmake numpy pybind11

:: Verify pybind11 installation and get its location
echo.
echo Verifying pybind11 installation...
python -c "import pybind11; print('pybind11 is installed at:', pybind11.get_cmake_dir())" > temp_path.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to find pybind11. Please make sure it's installed correctly.
    exit /b 1
)

set /p PYBIND11_PATH=<temp_path.txt
del temp_path.txt
echo %PYBIND11_PATH%

:: Verify EDSDK directory structure
echo.
echo Checking EDSDK directory structure...
if not exist "lib\EDSDK_64\Library" (
    echo ERROR: EDSDK library files not found in lib\EDSDK_64\Library
    echo Please make sure your Canon EDSDK files are properly installed.
    exit /b 1
)

if not exist "lib\EDSDK\Header" (
    echo ERROR: EDSDK header files not found in lib\EDSDK\Header
    echo Please make sure your Canon EDSDK files are properly installed.
    exit /b 1
)

:: Try to build the extension directly with pip
echo.
echo Building edsdk_bindings module...
echo.
echo This may take a few minutes...

:: Clean any previous build artifacts
if exist "build" (
    echo Cleaning previous build artifacts...
    rmdir /s /q build
)

:: Build with Python's setup.py and CMake
python setup.py build_ext --inplace

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build failed. Trying alternative method...
    echo.
    
    :: Create build directory
    mkdir build
    cd build
    
    :: Run CMake manually
    cmake .. -DCMAKE_PREFIX_PATH=%PYBIND11_PATH%
    
    if %ERRORLEVEL% NEQ 0 (
        cd ..
        echo.
        echo CMake configuration failed.
        echo Please make sure you have correctly installed pybind11.
        exit /b 1
    )
    
    cmake --build .
    
    if %ERRORLEVEL% NEQ 0 (
        cd ..
        echo.
        echo Build failed. Please check the error messages above.
        exit /b 1
    )
    
    cd ..
) else (
    echo.
    echo Build successful.
)

echo.
echo ==========================================
echo Build completed!
echo You can now use the cannon_wrapper module in your Python scripts.
echo ========================================== 