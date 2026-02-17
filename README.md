# Into the Breach save extractor

This is a experimental utility for extracting save files for the PC version of the game [Into the Breach](https://store.steampowered.com/app/590380/Into_the_Breach/) from the files of the Netflix cloud save slot.

In practice, it will be useful for transferring game progress from your Android device to your PC, since the PC version does not have the ability to synchronize saves with your Netflix account.

## Usage

For Windows:

- Copy the file `slot0.slot` to your **PC** from **Android** `/storage/emulated/0/Android/data/com.netflix.NGP.IntoTheBreach/files`;
- Switch **Steam** to offline mode;
- Make a backup save dir `%USERPROFILE%\Documents\My Games\Into The Breach`;
- Run in cmd:
    ```cmd
    python itb-save-extract.py slot0.slot "%USERPROFILE%\Documents\My Games\Into The Breach"
    ```
- Run game;
- Switch **Steam** to online mode.

## Disclaimer

> THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. In no event shall the author be liable for any claim, damages or other liability arising from, out of or in connection with the software or the use or other dealings in the software. Use it at your own risk. Always back up your data before using this tool.

Despite the fact that this utility works for me, I don’t know how it will behave on other versions of the game (my version is `1.2.90`), this is due to the fact that the purpose of many fields in file `slot0.slot` is still unknown. And the calculation of offsets may be incorrect.
