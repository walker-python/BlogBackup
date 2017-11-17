for /f "delims=" %%i in ('python build-env.py') do (set install=%%i&goto WORK) 

:WORK
@rem "%install%" install lib/setuptools-36.7.2-py2.py3-none-any.whl
@rem "%install%" install pyopenssl ndg-httpsclient pyasn1
@rem "%install%" install html5lib