import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRY = {
    "Documents": [".pdf", ".docx", ".txt", ".md", ".xlsx"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Media": [".jpg", ".png", ".mp4", ".mp3", ".wav"],
    "Scripts": [".py", ".sh", ".js"],
}


def compute_hash(file_path: Path) -> str:
  sha256 = hashlib.sha256()
  with open(file_path, "rb") as f:
    while chunk := f.read(8192):
      sha256.update(chunk)
  return sha256.hexdigest()


def organize_directory(target_dir: Path, dry_run: bool = False):
  target_dir = target_dir.resolve()
  archive_dir = target_dir / "_organized_archive"
  audit_log = target_dir / "audit_trail.jsonl"

  print(f"Scanning: {target_dir} (Dry Run: {dry_run})")

  for file_path in target_dir.iterdir():
    if file_path.is_dir() or file_path.name.startswith("."):
      continue

    ext = file_path.suffix.lower()
    matched_cat = "Unmatched"
    for cat, extensions in REGISTRY.items():
      if ext in extensions:
        matched_cat = cat
        break

    dest_folder = archive_dir / matched_cat
    if not dry_run:
      dest_folder.mkdir(parents=True, exist_ok=True)
      (archive_dir / "Duplicates").mkdir(parents=True, exist_ok=True)

    file_hash = compute_hash(file_path)
    destination = dest_folder / file_path.name

    action = "MOVE"
    if not dry_run and destination.exists():
      if compute_hash(destination) == file_hash:
        destination = archive_dir / "Duplicates" / file_path.name
        action = "DUPLICATE"
      else:
        destination = (
            dest_folder / f"{file_path.stem}_{file_hash[:8]}{file_path.suffix}"
        )
        action = "RENAME_COLLISION"

    print(f"[{action}] {file_path.name} -> {destination}")

    if not dry_run:
      file_path.rename(destination)
      log_entry = {
          "timestamp": datetime.now(timezone.utc).isoformat(),
          "action": action,
          "source": str(file_path),
          "destination": str(destination),
          "hash": file_hash,
      }
      with open(audit_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Lightweight registry-based file organizer."
  )
  parser.add_argument(
      "path", type=str, help="Target directory path to clean up"
  )
  parser.add_argument(
      "--dry-run", action="store_true", help="Simulate without moving files"
  )
  args = parser.parse_args()
  organize_directory(Path(args.path), dry_run=args.dry_run)
