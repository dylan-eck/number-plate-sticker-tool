# Number Plate Sticker Tool

## About:

A friend of mine helps run a local youth outreach program with the goal of  
teaching children how to mountain bike and providing oportunities for them to  
ride with groups of children of a similar ability level to their own. At the  
beginning of the program each summer, all of the children participate in a  
placement race to determine which group they should ride with. As each child  
crosses the finish line, a sticker is added to their number plate indicating  
which group they will be placed in. This python script takes as input an Excel  
file containing rows of information corresponding to what needs to be printed  
on each sticker. As output the script produces a series of pdf files that can  
be printed on 8.5x11 sheets of stickers.

## dependencies:

- [Python 3](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Pillow](https://python-pillow.org/)

Once python is installed, the rest of the dependencies can be installed using  
the following console command:

    python3 -m pip install -r requirements.txt

## usage:

The script can be run from the terminal by navigating to the directory  
containing the script and running the following command:

    python3 main.py

This will open a gui that can be used to adjust the output parameters and then  
generate the stickers.
