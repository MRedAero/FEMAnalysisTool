@ECHO OFF

:: Path that the python.exe is located. Note where the quotes are. This allows it to keep the spaces, but not the quotes
set "pypth=C:\CODE\WinPython-64bit-2.7.6.4\python-2.7.6.amd64\Lib\site-packages\PyQt4"

:: Exit if no drop
IF [%1] == [] (
    ECHO This tool quickly gathers the data necessary to generate a command line
    ECHO call to Python to use pyuic.py to convert a .ui file to a .py file.
    ECHO The new .py file will be created in the same folder as the .ui file dropped.
    pause
    GOTO :EOF )

:: Set dropped file to variable
SET qrcfile=%1

:: Get just the path, file name without extension and extension only of the input file
FOR %%f IN (%qrcfile%) DO (
    set pathonly=%%~dpf
    set flnameonly=%%~nf
    set extonly=%%~xf
    set filenmext=%%~nxf
    )

ECHO Saving to %pathonly%
ECHO Processing file %filenmext%

REM - pushd creates a temporary drive to handle locations on the server when the drive isn't mapped (\\na\shares\structure)	Avoids UNC path error
pushd %pathonly%

START "Converting UI to PY" /wait "%pypth%\pyrcc4.exe" -o "%flnameonly%_rc.py" "%qrcfile%"

REM - popd deletes the temporary drive
popd