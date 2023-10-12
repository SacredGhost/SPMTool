# SPMTool
A universal repository for the autosplitter, shared stats, and hide and seek

# SPM Auto Splitter
### vBeta3
An external auto splitter for Dolphin Emulator speedruns of Super Paper Mario. <br />
Supports all versions of the game, and since it's external, will support all timers that use hotkeys.

Currently Supports all main leaderboard categories! <br />
(Any%, Pit%, 100%, All Pixls, Defeat Shadoo)

### How to use
Simply launch Super Paper Mario on Dolphin, and open AutoSplitter.exe <br />
<br />
To change your hotkey split to match your LiveSplit, open settings.config and change the key to one of the provided key bindings. Make sure in your LiveSplit settings or on other timers, to have global hotkeys enabled. <br />
<br />
If your key is not on this list and you would like it added, please let me know or input a github issue. <br />
<br />
You can also set which extra splits to use in all runs, including if you want to split in each Pit% room.

### Credits
SeekyCt - For all of the reverse engineering of SPM, helping this process greatly <br />
JohnP55 - Creating read and write functions for DME and general code optimization <br />
NmFlash8 - NmFlash8

### To Do
Add options to change when to split (CastleSR timing, etc) <br />
Console Support (Wii U) <br />

Will most likely be changed from Python to C/C++ sometime in the future for REL modding.

### For Developers: 
Python 11 is not supported by dolphin memory engine. Must use Python 10.
