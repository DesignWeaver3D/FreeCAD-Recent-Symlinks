# FreeCAD Recent Symlinks

Symlinks your most recently modified FreeCAD projects into one folder, so the Start screen can show thumbnails without scanning your whole project archive.

## Why

FreeCAD's Start screen "Show additional folder" option does not scan subfolders. If your projects are spread across nested folders, the Start screen simply cannot show them. Pointing FreeCAD at a folder full of thousands of files also slows down thumbnail generation on boot.

This script scans your real project folder (recursively), finds the files with the most recent modification times, and creates symlinks to only those in a small destination folder. Point FreeCAD's Start screen at that destination folder instead.

## How it works

Each run:
1. Deletes every symlink currently in the destination folder.
2. Recursively scans the source folder for `.FCStd` files.
3. Sorts them by last modified time.
4. Creates fresh symlinks in the destination folder for the newest `MAX_PROJECTS` files.

Nothing in the source folder is touched. The destination folder is treated as fully disposable and rebuilt from scratch each run.

## Setup

1. Open `sync_fcstd_symlinks.py` and edit:
   - `SOURCE_DIR`: the folder containing your FreeCAD projects (can contain subfolders).
   - `TARGET_DIR`: an empty local folder to hold the symlinks. Avoid cloud-synced folders (OneDrive, Dropbox, etc), they can mishandle symlinks.
   - `MAX_PROJECTS`: how many recent files to keep symlinked. Higher numbers mean more thumbnails but a slower Start screen. 50 is a reasonable starting point.

2. In FreeCAD, go to Edit → Preferences → Start, and set "Show additional folder" to your `TARGET_DIR`.

3. Run the script once manually to confirm it works:
   ```
   python sync_fcstd_symlinks.py
   ```

### Windows: symlink permissions

Creating symlinks on Windows normally requires administrator rights. To avoid running as admin every time, enable Developer Mode: Settings → Privacy & Security → For Developers → toggle on Developer Mode. A reboot may be required for it to take effect.

If your source folder is a network share, symlinking directly across two network locations can be blocked by Windows policy. Keeping the destination folder local (as recommended above) avoids this entirely.

If your source folder is on a network drive, use its full UNC path (e.g. `\\SERVERNAME\ShareName\Folder`) rather than a mapped drive letter (e.g. `Z:\Folder`). Mapped drive letters are tied to your interactive login session and are often not visible when the script runs under Task Scheduler, even when set to run only when logged on.

### Scheduling

The script needs to run periodically to stay in sync, it does not run automatically inside FreeCAD.

- **Windows**: use Task Scheduler. Point the action at your `python.exe` path, with the script's full path as the argument. Trigger it at logon or on an interval.
- **Linux/macOS**: use `cron` or `launchd` to run the script on a schedule.

## Notes

- Tested on Windows. The core logic (`os.symlink`, `pathlib`) is standard Python and should work on Linux and macOS as well, though the symlink permission caveats above are Windows-specific.
- Filenames that repeat across different subfolders will only be symlinked once; duplicates are skipped and logged.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
