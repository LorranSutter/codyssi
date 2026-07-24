#!/usr/bin/env python3
"""
Scans all problem folders and generates progress summaries:
- Root README.md: overall stats + progress bars per year
- year/README.md: detailed problem tables with stars

For each problem's main.py, it checks whether part1(), part2(), part3() contain
"pass" as the first non-empty line of the function body. If so, the part is
considered unsolved.

The root summary is injected between <!-- SUMMARY:START --> and <!-- SUMMARY:END -->
markers in README.md, preserving all other content.

Each year/README.md is managed between <!-- SUMMARY:START --> and
<!-- SUMMARY:END --> markers as well, so any content outside the markers
(like the title) is preserved after the first run.
"""

import re
from pathlib import Path


ROOT = Path(__file__).parent

# Known total problem counts per year/round. Years not listed here fall back
# to the highest problem number discovered on disk for that year.
KNOWN_TOTALS = {
    "2024": 4,   # Summer at the Lab (sample round)
    "2025": 18,  # Journey to Atlantis
}

# Round titles per year, shown alongside the year in headers/links. Years not
# listed here are shown as a bare year.
YEAR_TITLES = {
    "2024": "Summer at the Lab",
    "2025": "Journey to Atlantis",
}


def get_year_label(year: str) -> str:
    """Returns 'year — Title' if a title is known, otherwise just 'year'."""
    title = YEAR_TITLES.get(year)
    return f"{year} — {title}" if title else year


def find_problems(root: Path) -> dict:
    """
    Returns a nested dict: {year: {problem_number: {part: solved}}}
    """
    results = {}

    for year_dir in sorted(root.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        year = year_dir.name

        for problem_dir in sorted(year_dir.iterdir()):
            if not problem_dir.is_dir():
                continue
            match = re.match(r"problem(\d+)", problem_dir.name)
            if not match:
                continue

            problem_num = int(match.group(1))
            main_file = problem_dir / "main.py"
            if not main_file.exists():
                continue

            parts = check_parts(main_file)
            results.setdefault(year, {})[problem_num] = parts

    return results


def check_parts(main_file: Path) -> dict:
    """
    Parses main.py and checks if part1/part2/part3 functions still contain
    the unsolved stub left by new_problem.sh: a "# TODO" marker on the first
    line of the body, or (for problems scaffolded before that convention) a
    body that is just a bare "pass".
    Returns {1: True/False, 2: True/False, 3: True/False} where True = solved.
    """
    content = main_file.read_text()
    parts = {}

    for part_num in [1, 2, 3]:
        pattern = rf"def part{part_num}\(.*?\):\s*\n(.*?)(?=\ndef |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            parts[part_num] = False
            continue

        body = match.group(1)
        non_empty_lines = [line.strip() for line in body.split("\n") if line.strip()]
        first_code_line = non_empty_lines[0] if non_empty_lines else ""

        is_todo_stub = "# TODO" in first_code_line
        is_bare_pass_stub = non_empty_lines == ["pass"]

        parts[part_num] = not (is_todo_stub or is_bare_pass_stub)

    return parts


def get_total_problems(year: str, discovered_max: int) -> int:
    """Returns the expected total number of problems for the given year."""
    return KNOWN_TOTALS.get(year, discovered_max)


def generate_root_summary(results: dict) -> str:
    """Generates the root README summary with progress bars per year."""
    lines = []
    lines.append("## 📊 Progress")
    lines.append("")

    total_solved = 0
    total_parts = 0

    section_lines = []

    for year in sorted(results.keys()):
        problems = results[year]

        solved = sum(
            1 for p in problems.values() for part, s in p.items() if s
        )
        total_problems = get_total_problems(year, max(problems.keys(), default=0))
        total = total_problems * 3
        total_solved += solved
        total_parts += total

        pct = (solved / total * 100) if total > 0 else 0
        unsolved = total - solved
        bar = "█" * solved + "░" * unsolved

        section_lines.append(f"### [{get_year_label(year)}](./{year}/)")
        section_lines.append("")
        section_lines.append(f"`{bar}` **{solved}/{total}** parts solved ({pct:.0f}%)")
        section_lines.append("")

    # Overall summary
    overall_pct = (total_solved / total_parts * 100) if total_parts > 0 else 0
    lines.append(f"> **Overall: {total_solved}/{total_parts} parts solved ({overall_pct:.0f}%)**")
    lines.append("")
    lines.extend(section_lines)

    return "\n".join(lines)


def generate_year_readme(year: str, problems: dict) -> str:
    """Generates the problem table for a year README."""
    total_problems = get_total_problems(year, max(problems.keys(), default=0))
    solved = sum(1 for p in problems.values() for part, s in p.items() if s)
    total = total_problems * 3
    pct = (solved / total * 100) if total > 0 else 0
    unsolved = total - solved
    bar = "█" * solved + "░" * unsolved

    lines = []
    lines.append(f"`{bar}` **{solved}/{total}** parts solved ({pct:.0f}%)")
    lines.append("")
    lines.append("| Problem | Part 1 | Part 2 | Part 3 |")
    lines.append("|:--------|:------:|:------:|:------:|")

    max_problem = max([total_problems] + list(problems.keys()))
    for problem_num in range(1, max_problem + 1):
        if problem_num in problems:
            parts = problems[problem_num]
            cols = []
            for p in [1, 2, 3]:
                cols.append("⭐" if parts.get(p, False) else "⬚")
            lines.append(
                f"| [Problem {problem_num:02d}](./problem{problem_num:02d}/) | {cols[0]} | {cols[1]} | {cols[2]} |"
            )
        else:
            lines.append(
                f"| Problem {problem_num:02d} | ⬚ | ⬚ | ⬚ |"
            )

    lines.append("")
    return "\n".join(lines)


def inject_between_markers(content: str, summary: str, default_header: str) -> str:
    """
    Replaces content between <!-- SUMMARY:START --> and <!-- SUMMARY:END --> markers.
    If markers don't exist, creates the file with a header + markers.
    """
    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"
    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        return pattern.sub(block, content)
    else:
        # No markers yet — create with default header
        return f"{default_header}\n\n{block}\n"


def update_root_readme(root: Path, summary: str, total_solved: int) -> None:
    """Injects the summary and badge into the root README.md between markers."""
    readme_path = root / "README.md"
    content = readme_path.read_text()

    # 1. Update the badge first
    badge_start = "<!-- BADGE:START -->"
    badge_end = "<!-- BADGE:END -->"
    badge_content = f"{badge_start}[![Solved Challenges](https://img.shields.io/badge/Solved%20Challenges-{total_solved}-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://www.codyssi.com/){badge_end}"

    if badge_start in content and badge_end in content:
        pattern = re.compile(
            re.escape(badge_start) + r".*?" + re.escape(badge_end),
            re.DOTALL,
        )
        content = pattern.sub(badge_content, content)

    # 2. Update the progress section
    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"
    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        new_content = pattern.sub(block, content)
    else:
        # Insert after the intro paragraph
        intro_pattern = re.compile(
            r"(# .+\n\n.+\n\n.+\n)"
        )
        match = intro_pattern.match(content)
        if match:
            insert_pos = match.end()
            new_content = (
                content[:insert_pos] + "\n" + block + "\n\n" + content[insert_pos:]
            )
        else:
            new_content = content + "\n\n" + block + "\n"

    readme_path.write_text(new_content)
    print(f"✅ Updated {readme_path}")


def update_year_readme(root: Path, year: str, table_summary: str) -> None:
    """Creates or updates the year/README.md with the problem table."""
    readme_path = root / year / "README.md"
    default_header = f"# {get_year_label(year)}"

    if readme_path.exists():
        content = readme_path.read_text()
    else:
        content = ""

    new_content = inject_between_markers(content, table_summary, default_header)
    readme_path.write_text(new_content)
    print(f"✅ Updated {readme_path}")


def main():
    results = find_problems(ROOT)

    # Calculate total solved parts
    total_solved = sum(
        1 for problems in results.values() for parts in problems.values() for part_solved in parts.values() if part_solved
    )

    # Generate and update root README
    root_summary = generate_root_summary(results)
    update_root_readme(ROOT, root_summary, total_solved)

    # Generate and update each year README
    for year in sorted(results.keys()):
        problems = results[year]
        table_summary = generate_year_readme(year, problems)
        update_year_readme(ROOT, year, table_summary)


if __name__ == "__main__":
    main()
