# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

import os
from pathlib import Path

# Configured paths (edit these to match your own folders)
SOURCE_DIR = Path(r"PATH_TO_YOUR_PROJECT_FOLDER").resolve()
TARGET_DIR = Path(r"PATH_TO_YOUR_DESTINATION_FOLDER").resolve()

# Max number of most recently modified projects to keep symlinked
MAX_PROJECTS = 100


def sync_fcstd_symlinks():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 1. WIPE: Remove every existing symlink in the target folder
    for item in TARGET_DIR.iterdir():
        if item.is_symlink():
            try:
                item.unlink()
            except Exception as e:
                print(f"[Sync] Failed to remove old link {item.name}: {e}")

    # 2. SCAN: Find all fcstd files and their modified times
    candidates = []
    for fcstd_file in SOURCE_DIR.rglob("*"):
        if fcstd_file.suffix.lower() != ".fcstd":
            continue
        fcstd_file = fcstd_file.resolve()
        if TARGET_DIR in fcstd_file.parents:
            continue
        try:
            mtime = fcstd_file.stat().st_mtime
        except Exception as e:
            print(f"[Sync] Could not read {fcstd_file}: {e}")
            continue
        candidates.append((mtime, fcstd_file))

    # 3. SORT: Newest first, keep only MAX_PROJECTS
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    newest = candidates[:MAX_PROJECTS]

    # 4. CREATE: Symlink the selected files, skipping duplicate names
    seen_names = set()
    for _, fcstd_file in newest:
        if fcstd_file.name in seen_names:
            print(f"[Sync] Skipped duplicate filename: {fcstd_file}")
            continue
        seen_names.add(fcstd_file.name)

        link_path = TARGET_DIR / fcstd_file.name
        try:
            os.symlink(fcstd_file, link_path)
            print(f"[Sync] Created symlink for: {fcstd_file.name}")
        except OSError as e:
            print(f"[Sync] Could not create link for {fcstd_file.name}: {e}")


if __name__ == "__main__":
    sync_fcstd_symlinks()
