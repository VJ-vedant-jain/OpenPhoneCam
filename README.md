# OpenPhoneCam

FOSS program that turns your phone into a high quality webcam for your computer!

# Disclaimer

This is a work-in-progress app that is right now using scrcpy to fetch the video from your android device but eventually we will move over to a native android app and companion server.

This project started out because I was fed up with those phone webcam apps relying on OBS and needing payment and limiting the resolution and other problems i just didnt like. im all for supporting developers and huge respect to those devs for doing this, but i mean if i have the ability to just... do it myself and learn many libraries and android app development simultaneously then might as well...

This project is NOT COMPLETE. Attempting to run it will give you...nothing.


# Requirements

After a functional release, we will update this part.

# Notes for future

What’s Done:

Made a new UI section (cammy.ui) – will be linked with mainWindow.ui as a tab
Added camera preview using OpenCV – need to figure out how to intercept a web stream via local IP and display it as video
Start/Stop camera from buttons
Set FPS and resolution from the UI
Mirror video horizontally and vertically
Aspect ratio options with cropping
Status messages show what’s happening
Save and load all settings to/from a JSON file
Added menu actions: Save, Load, Exit
Split code into multiple files: main.py, window.py, camera.py, settings.py
Timer updates the video feed continuously
All UI elements hooked up to real functionality (line edits, spin boxes, checkboxes, combo boxes)

Currently Pending:

Audio options, connection with mobile, better logging and error handling
About/Documentation options in Help tab
Linking cammy.ui with mainWindow.ui
