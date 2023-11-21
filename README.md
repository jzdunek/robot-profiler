robot-profiler
==============

A Profiler for the Robot Framework.

This is the Python 3.x fork of the original project [jzdunek/robot-profiler](https://github.com/jzdunek/robot-profiler).

This fork has been tested with **Python 3.11** on **Windows 11** and is compatible with **Robot Framework 6.1.1**.
No guarantees are made beyond that.

It is likely not compatible with Robot Framework 7+,
because the time format in `output.xml` will most likely be changed for that major version.
That should only require a change in the method `calc_elapsed_time`, though.

Overview
--------
The Robot Profiler analysis the output.xml file generated
during test runs by the Robot Framework. It calculates
the overall runtime, the average runtime, and the number
of calls on a "per keyword" level. The calculated data
are written to a file for later use with a spreadsheet.

Pre-requisites
--------------
* Python 3.x

Pre-requisites for running the automated tests
----------------------------------------------
* Python 3.x
* Robot Framework in PYTHONPATH
* Project's source folder (src/python) in PYTHONPATH

Installation
------------
Copy the file `robot_profiler.py` into the module search path of your
python installation.

Sorry, but no easy_setup or pip support at this time...

Usage
-----
```
usage: robot_profiler.py [-h] [-e ENCODING] [-s SEPARATOR] [-l LOCALE]
                         file_name [file_name ...]
```
```
positional arguments:
  file_name             List of input files. If last file in list does not
                        have xml as extension this file will be used as output
                        file.
```
```
optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding for output file.
  -s SEPARATOR, --separator SEPARATOR
                        Separator used in output file.
  -l LOCALE, --locale LOCALE
                        Locale used for number formatting.
```
You can pass a list of file names a positional arguments behind the named arguments. The Robot Profiler
will treat all files as output.xml files from the Robot Framework. If the last file of the given list
does not have .xml as extension that file name will be used as output file name for the Robot Profiler.
Otherwise, the path and the basename of the first file name in the list will be used as the output
file name with `.csv` as the new extension. The command behaves this way to keep the commandline
compatible with release 1.0.0.

When passing multiple output xml files to the Robot Profiler it will read all files and aggregate the
data into one output file.

Parameters `-e`, `-s`, and `-l` are optional. They can be used to set the file encoding,
the field separator and the localization of the number format. The default values for these parameters
are chosen as sensible as possible and create a csv file that can be opened using Excel: it
uses cp1252 as encoding (Windows standard), and semicolon as field separator. If you need a
TSV file (tab separated values) you can use `-s \t`. The localization option uses no explicit
default value - it uses the platform's default locale. Please note that valid values for `-l`
might be platform depending. E.g. a german locale is `de_DE` on Linux but `German` on Windows...

Running the unit tests
----------------------
The unit tests require that you installed the Robot Framework properly.
Basically this means that the Robot Framework must be in your PYTHONPATH. Additionally, the project's
source folder `src/python` must be in your PYTHONPATH.

For running the unit tests change the current directory to the test folder `test/python` and execute the
following command:

`python -m unittest robot_profiler_unittests`

If you prefer test discovery the command is:

`python -m unittest discover -p *.py`

Running the integration tests
-----------------------------
The project contains integration tests automated with the Robot Framework. Thus, the Robot Framework needs to be
installed. Additionally, the project's source folder `src/python` must be in your PYTHONPATH.

For running the integration test change the current directory to the test folder `test/robot` and execute the
following command:

`python -m robot.run robot_profiler_integrationtests.robot`
