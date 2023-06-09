# AutoInventory

## Introduction

I work at a Pizza Hut where, every week and at the end of every month, we count inventory.
The process went a little something like this:

1. Count items and write them down on paper
2. Enter the numbers into an Excel spreadsheet
3. Print out the Excel spreadsheet
4. Enter the numbers into eResturant that will be sent to corporate, which involved:
    1. Enter the item ID in the search bar
    2. Enter the item count in the correct box
    3. Repeat steps 1 and 2 for all ~70 items (or more for other stores)

I noticed this extremely tedious process my manager would have to endure every week, and that she was quite a few weeks behind on it.
I found it a little crude that you had to enter the same numbers into the computer twice in two seperate places,
so I created this script that would automate step 4, making step 3 obsolete.
Now the process is like this:

1. Count items and write them down on paper
2. Enter the numbers into an Excel spreadsheet
3. Run AutoInventory and watch the magic happen!

I created a functioning prototype for this script after a couple days of research and testing followed by one day of work.
I have been polishing it ever since.

## What AutoInventory does and how it does it

In simple terms, AutoInventory reads a spreadsheet file containing inventory data and enters the data into the eResturant website automatically.

It uses two main libraries to accomplish this:

- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/index.html) for reading from the spreadsheet
- [Splinter](https://splinter.readthedocs.io/en/latest/index.html) for browser control automation

Other important libraries include:

- [ConfigParser](https://docs.python.org/3/library/configparser.html) for reading the config file
- [PySimpleGUI](https://www.pysimplegui.org/en/latest/) for the GUI
- [PyInstaller](https://pyinstaller.org/en/stable/index.html) for generating the executable
- [Inno Setup](https://jrsoftware.org/isinfo.php) for generating the installer

## Future plans

- [ ] Password hashing so that the eResturant password is not stored in plaintext
- [ ] Allow the user to modify what columns in the spreadsheet the data will be read from.
This will allow for any spreadsheet layout to be used as long as the 4 columns are accounted for
- [ ] Add the logo to the GUI
- [ ] Fix a bug where the program can't tell the difference between what message is popping up.
In cases where the previous inventory sheet has not been posted this will cause a crash because the program will think the message says the created inventory sheet already exists
- [ ] Error handling/detection for when the inventory sheet cannot be saved
- [x] Create a setup GUI
- [x] Settings menu GUI for updating username/password and other things
- [ ] Help menu that explains certain settings and behavior
- [ ] The settings menu automatically opens if your eResturant password has changed
- [ ] Default date to most recent Sunday/End of most recent month
- [x] Detection for when the username and password are not set
- [ ] Investigate possible problem that could arrise when waiting for page to load
- [ ] Change 'items' to 'elements' in relation to find_and_click
- [ ] More error handling in the event that find_and_click fails
- [ ] Add more comments on what specifically is being clicked on at each part
- [ ] Make units case insensitive
- [x] Installer
  - [x] Windows 7 installer
  - [x] Add README to installer
- [x] Automated updates
  - [x] Create script
  - [x] Compress that one series of elifs in the script
  - [x] Update.exe PyInstaller script
  - [x] Add exe to installer
  - [x] Implement exe into the main program
  - [x] Windows 7 support for updater
  - [x] Have the updater take LEGACY as a parameter
- [ ] Make the updater actually detect if there's a new version available rather than just changing a text file on remote
- [x] Hide command prompt window
- [ ] Internalize VERSION file
- [ ] Future proof the updater so that it can update itself if need be
- [ ] Ability for the updater to update the config if new fields are added while keeping information intact
- [x] Config reorganization
- [x] Automatically open log.txt after running
- [ ] Warning if a selected date is far in the past or in the future
- [ ] Have installer rename and use default configs
- [ ] Make the units in the log file more concise
- [ ] Add a sample spreadsheet to the repository
- [ ] (Maybe) Revamp/modernize the GUI
- [ ] (Maybe) replace find_and_click function parameters with booleans instead of a string
- [ ] (Maybe) create some unit tests
- [ ] (Maybe) allow users to create their own exceptional behavior for certain items
(such as searching for a different code than what is provided or using a different unit).
Though this may be complicated and difficult for the user to understand how it works
- [ ] (Maybe) add something that detects if there are warnings in eResturant
- [ ] (Maybe) do some CI/CX shenanigans
- [ ] (Maybe) have a status bar that shows what the program is doing and its progress
