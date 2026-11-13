# Quick File Cleaner (`quick-file-cleaner`)

A lightweight, robust, zero-dependency CLI utility written in Python for automated file organization, SHA-256 duplicate detection, and structured audit logging. Designed for developers and power users who want local file hygiene without bloated software or external package dependencies.






## Features
* Registry-Based Classification: Decouples routing logic from file extension mappings. Easily extend categories or add custom rules via a clean configuration dictionary.

* Content-Based Duplicate Detection: Computes cryptographic SHA-256 hashes to catch identical files regardless of naming differences, safely quarantining duplicates.

* Smart Collision Resolution: Automatically handles name collisions by appending short hash suffixes to prevent accidental file overwrites.

* Safe Dry-Run Mode (--dry-run): Simulate organization runs and preview actions in the console before making any actual file system changes.

* Immutable Audit Trail: Logs every file move, duplicate capture, and operation timestamp to a structured JSON Lines (audit_trail.jsonl) file.

* Zero Dependencies: Built exclusively using Python's robust standard library (pathlib, hashlib, json, argparse), making it ultra-portable across Linux, macOS, and Windows.






## Requirements
* Python 3.8 or higher.




## Installation & Setup
1. Clone or download this repository locally:

```Bash
git clone https://github.com/ananyaja/quick-file-cleaner.git
cd quick-file-cleaner
```
2. Ensure the script is executable (Linux/macOS):

```Bash
chmod +x cleaner.py
```

## Usage
Run the script from the command line by passing the target directory path you want to organize.

### 1. Simulate a Cleanup (Dry Run)
Preview what actions the script will take without moving any files:

```Bash
python cleaner.py /path/to/target/folder --dry-run
```
### 2. Execute Organization
Run the cleaner to sort files into archive categories, isolate duplicates, and generate the audit log:

```Bash
python cleaner.py /path/to/target/folder
```
##Directory Structure After Organization
When run on a target folder, the script automatically generates a clean archive structure:

```
/path/to/target/folder/
├── _organized_archive/
│   ├── Documents/      # .pdf, .docx, .txt, .md, .xlsx
│   ├── Archives/       # .zip, .tar, .gz, .rar
│   ├── Media/          # .jpg, .png, .mp4, .mp3
│   ├── Scripts/        # .py, .sh, .js
│   ├── Unmatched/      # Files with unmapped extensions
│   └── Duplicates/     # Exact content duplicates quarantined safely
└── audit_trail.jsonl   # Detailed JSON execution log
```

##License
Distributed under the MIT License. See LICENSE for more information.
