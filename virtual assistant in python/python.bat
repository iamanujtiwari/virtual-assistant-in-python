@echo on
REM Install required Python packages

echo Installing speech_recognition...
pip install SpeechRecognition

echo Installing pyttsx3...
pip install pyttsx3

echo Installing pywhatkit...
pip install pywhatkit

echo Installing wikipedia-api...
pip install wikipedia-api

echo installing bs4-api....
pip install bs4-api

echo installing pil -api ...
pip install pil -api

echo datetime and webbrowser are part of the standard library and do not need installation.
echo random is also part of the standard library and does not need installation.

echo All required packages installed.

REM Wait for 5 seconds before closing
timeout /t 5 /nobreak

REM Close the Command Prompt window
exit
