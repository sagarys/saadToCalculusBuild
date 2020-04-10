echo "copying....."
ROBOCOPY %1 %2 /S /SEC /R:1 /W:1 /DCOPY:T /LOG:%3﻿
echo "copied !!!!!!!!"

IF %ERRORLEVEL% NEQ 1 ( 
   echo "Error While Copying directory" 
   EXIT 1
)

EXIT 0