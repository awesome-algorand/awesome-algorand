#!/usr/bin/env python3
"""
Script to process link checker reports and move dead links to archived.md.
"""

import json
from pathlib import Path
import re
import argparse
from datetime import datetime
from collections import defaultdict


def parse_lychee_report(report_path):
    """Parse the lychee JSON report and return a set of failed URLs."""
    failed_urls = set()

    try:
        Path(report_path).touch()
        content = Path(report_path).read_text(encoding="utf-8").strip()
        if not content:
            print(f"Warning: Report file {report_path} is empty.")
            return failed_urls

        data = json.loads(content)

        # Lychee format changed in newer versions - handle both formats
        if "data" in data and "failed" in data["data"]:
            # New format: {"data": {"failed": [{"url": "...", ...}]}}
            for item in data["data"]["failed"]:
                if "url" in item:
                    failed_urls.add(item["url"])
        else:
            # Old format: {"url1": {"status": "..."}, "url2": ...}
            for url, details in data.items():
                if isinstance(details, dict) and details.get("status") != "alive":
                    failed_urls.add(url)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading report file: {e}")
        return failed_urls

    return failed_urls


def load_link_history(history_path=".github/link-history.json"):
    """Load link failure history from a JSON file."""
    path = Path(history_path)
    if not path.exists():
        return defaultdict(int)

    try:
        return defaultdict(int, json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, FileNotFoundError):
        return defaultdict(int)


def save_link_history(history, history_path=".github/link-history.json", dry_run=False):
    """Save link failure history to a JSON file."""
    if dry_run:
        print("[DRY RUN] Would save link history to", history_path)
        print("[DRY RUN] Link history:", json.dumps(history, indent=2))
        return

    path = Path(history_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(json.dumps(history, indent=2), encoding="utf-8")


def process_markdown_files(
    readme_path, archive_path, failed_urls, link_history, dry_run=False
):
    """
    Process README.md, moving items with persistent failed links to archived.md.
    Returns list of archived URLs.
    """
    # Identify links that have failed 3 or more times
    urls_to_archive = {
        url for url, count in link_history.items() if count >= 3 and url in failed_urls
    }

    if not urls_to_archive:
        print("No links have failed 3 or more times. No changes needed.")
        return []

    print(f"Links to archive: {urls_to_archive}")

    readme = Path(readme_path)
    try:
        readme_lines = readme.read_text(encoding="utf-8").splitlines(keepends=True)
    except FileNotFoundError:
        print(f"Error: README file not found at {readme_path}")
        return []

    # Process the README.md to extract list items containing failed URLs
    new_readme_lines = []
    archived_items = []
    archived_urls = []

    # Track multi-line list items
    in_list_item = False
    current_item_lines = []

    for line in readme_lines:
        is_list_start = re.match(r"^- ", line.strip())

        # Handle start of a new list item
        if is_list_start:
            # Process previous list item if we were tracking one
            if in_list_item and current_item_lines:
                item_content = "".join(current_item_lines)
                should_archive = False
                found_url = None

                # Check if this item contains any URL to archive
                for url in urls_to_archive:
                    # Check for URL in markdown links [text](url) or bare URLs
                    if re.search(
                        rf"(\[.*?\]\({re.escape(url)}\))|{re.escape(url)}", item_content
                    ):
                        should_archive = True
                        found_url = url
                        break

                if should_archive and found_url:
                    archived_items.extend(current_item_lines)
                    archived_urls.append(found_url)
                    print(f"Archiving item with URL: {found_url}")
                else:
                    new_readme_lines.extend(current_item_lines)

            # Start tracking new list item
            in_list_item = True
            current_item_lines = [line]

        # Continue tracking current list item if we're in one
        elif in_list_item and (line.strip() == "" or line.startswith("  ")):
            current_item_lines.append(line)

        # End of a list item, process it
        elif in_list_item:
            item_content = "".join(current_item_lines)
            should_archive = False
            found_url = None

            # Check if this item contains any URL to archive
            for url in urls_to_archive:
                if re.search(
                    rf"(\[.*?\]\({re.escape(url)}\))|{re.escape(url)}", item_content
                ):
                    should_archive = True
                    found_url = url
                    break

            if should_archive and found_url:
                archived_items.extend(current_item_lines)
                archived_urls.append(found_url)
                print(f"Archiving item with URL: {found_url}")
            else:
                new_readme_lines.extend(current_item_lines)

            # Reset list item tracking and add current line
            in_list_item = False
            current_item_lines = []
            new_readme_lines.append(line)

        # Not a list item, just keep the line
        else:
            new_readme_lines.append(line)

    # Process last list item if we ended while tracking one
    if in_list_item and current_item_lines:
        item_content = "".join(current_item_lines)
        should_archive = False
        found_url = None

        for url in urls_to_archive:
            if re.search(
                rf"(\[.*?\]\({re.escape(url)}\))|{re.escape(url)}", item_content
            ):
                should_archive = True
                found_url = url
                break

        if should_archive and found_url:
            archived_items.extend(current_item_lines)
            archived_urls.append(found_url)
            print(f"Archiving item with URL: {found_url}")
        else:
            new_readme_lines.extend(current_item_lines)

    # If no items were archived, return
    if not archived_items:
        print("No items need to be archived.")
        return []

    # In dry run mode, just show what would be changed
    if dry_run:
        print("\n[DRY RUN] Changes that would be made:")
        print(
            f"[DRY RUN] {len(archived_urls)} items would be moved from "
            f"{readme_path} to {archive_path}"
        )
        print("[DRY RUN] URLs to be archived:")
        for url in archived_urls:
            print(f"[DRY RUN]   - {url}")

        print("\n[DRY RUN] Items that would be archived:")
        for item in archived_items:
            print(f"[DRY RUN]   {item.rstrip()}")

        return archived_urls

    # Update README.md with items containing failed links removed
    Path(readme_path).write_text("".join(new_readme_lines), encoding="utf-8")

    # Add archived items to archived.md
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Create or append to archived.md
    archive = Path(archive_path)
    mode = "a"  # Append by default
    header = f"\n\n## Archived on {timestamp}\n\n"

    if not archive.exists() or archive.stat().st_size == 0:
        # Create new file with header
        mode = "w"
        header = (
            f"# Archived Entries\n\n"
            f"Entries moved here due to persistently failing links detected by the "
            f"automated link checker.\n\n"
            f"## Archived on {timestamp}\n\n"
        )

    with archive.open(mode, encoding="utf-8") as f:
        f.write(header)
        f.writelines(archived_items)

    # Reset failure count for archived URLs in the history
    for url in archived_urls:
        if url in link_history:
            link_history[url] = 0  # Reset count once archived

    # Save list of archived URLs to a file for PR deduplication
    if archived_urls:
        archive_urls_file = Path(".github/archived_urls.txt")
        archive_urls_file.parent.mkdir(parents=True, exist_ok=True)
        archive_urls_file.write_text("\n".join(archived_urls) + "\n", encoding="utf-8")

    return archived_urls


def main():
    parser = argparse.ArgumentParser(
        description="Process link checker reports and handle dead links"
    )
    parser.add_argument("report", help="Path to the lychee report JSON file")
    parser.add_argument("readme", help="Path to the README.md file to process")
    parser.add_argument("archive", help="Path to the archived.md file to create/update")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no changes written)",
    )
    parser.add_argument(
        "--force-count",
        type=int,
        help="Force failure count for specified URLs (for testing)",
    )
    parser.add_argument(
        "--force-urls",
        nargs="+",
        help="URLs to force the failure count on (for testing)",
    )

    args = parser.parse_args()

    # Parse the report to get failed URLs
    failed_urls = parse_lychee_report(args.report)
    print(f"Found {len(failed_urls)} failed URLs")

    # Load link history
    link_history = load_link_history()

    # Force failure count for test URLs if specified
    if args.force_count and args.force_urls:
        for url in args.force_urls:
            link_history[url] = args.force_count
            # Also add to failed URLs if not present
            failed_urls.add(url)
        print(
            f"Forced failure count {args.force_count} for {len(args.force_urls)} URLs"
        )
    else:
        # Update failure count for each failed URL
        for url in failed_urls:
            link_history[url] += 1

    # Process the markdown files and archive links that failed 3+ times
    process_markdown_files(
        args.readme, args.archive, failed_urls, link_history, args.dry_run
    )

    # Save updated link history
    save_link_history(link_history, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
