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

## Future plans

- Password hashing so that the eResturant password is not stored in plaintext
- Allow the user to modify what columns in the spreadsheet the data will be read from.
This will allow for any spreadsheet layout to be used as long as the 4 columns are accounted for
- Create an instruction text file for setting up and running the program
- Possibly add a logo to the GUI
- Fix a bug where the program can't tell the difference between what message is popping up.
In rare cases when the previous inventory sheet has not been posted this will cause a crash because the program will think the message says the created inventory sheet already exists
- Error handling/detection for when the inventory sheet cannot be saved
- Possibly create some unit tests
- Possibly allow users to create their own exceptional behavior for certain items (such as searching for a different code than what is provided or using a different unit).
Though this may be complicated and difficult for the user to understand how it works
- Possibly create a setup GUI
- Default date to most recent Sunday/End of most recent month
- Detection for when the username and password are not set
- Investigate possible problem that could arrise when waiting for page to load
- Maybe replace find_and_click function parameter with booleans instead of a string
- Change 'items' to 'elements' in relation to find_and_click
- More error handling in the event that find_and_click fails
- Add more comments on what specifically is being clicked on at each part
- Make units case insensitive
- Maybe something that detects if there are warnings in eResturant
- Maybe automated updates
