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

Merged ui files for one seamless gui
refactored code into multiple files
old code stored in a folder for reference (required for tab_main.py functionality)

Currently Pending:

Audio options, connection with mobile, better logging and error handling
tab_main.py functionality
tab_settings.py functionality + ui
tab_about.py functionality + ui

Add options in settings to change theme of ui. Current GUI defaults to Fusion theme instead of the system Breeze theme. 
Unable to make pyqt use breeze theme unless adding device specific code. One way to counter is to use QSS files for the ui. 
Would even provide consistent ui across different devices but cannot find good ones. Will take time to find good ones or will have to write our own (too hectic tbh). First option is to find some online but if nothing works, we may have to make one ourselves.