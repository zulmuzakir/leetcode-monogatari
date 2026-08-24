#!/usr/bin/env python3
"""Runner: compile-and-run solutions by problem number or path.

C++ and Python solutions are first-class: dispatch is by file extension, and
a problem folder may hold both languages (disambiguate with --lang). The
repository root is the directory containing this script. Build artifacts are
confined to the ignored .build directory.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / ".build"
TRACKS = ("neetcode150", "general")
PROBLEM_FOLDER = re.compile(r"^(\d+)_.+")
SOLUTION_FILES = ("solution.cpp", "solution.py")
PROGRESS_START = "<!-- progress:start -->"
PROGRESS_END = "<!-- progress:end -->"

# NeetCode 150 curriculum: category folder name, display name, problem total.
# Row order in the generated progress table follows this tuple, not the disk.
CURRICULUM = (
    ("01_arrays_hashing", "Arrays & Hashing", 9),
    ("02_two_pointers", "Two Pointers", 5),
    ("03_sliding_window", "Sliding Window", 6),
    ("04_stack", "Stack", 7),
    ("05_binary_search", "Binary Search", 7),
    ("06_linked_list", "Linked List", 11),
    ("07_trees", "Trees", 15),
    ("08_tries", "Tries", 3),
    ("09_heap_priority_queue", "Heap / Priority Queue", 7),
    ("10_backtracking", "Backtracking", 9),
    ("11_graphs", "Graphs", 13),
    ("12_advanced_graphs", "Advanced Graphs", 6),
    ("13_1d_dynamic_programming", "1D Dynamic Programming", 12),
    ("14_2d_dynamic_programming", "2D Dynamic Programming", 11),
    ("15_greedy", "Greedy", 8),
    ("16_intervals", "Intervals", 6),
    ("17_math_geometry", "Math & Geometry", 8),
    ("18_bit_manipulation", "Bit Manipulation", 7),
)
CURRICULUM_DIRS = {dirname for dirname, _, _ in CURRICULUM}


def fail(message: str) -> int:
    print(f"run.py: {message}", file=sys.stderr)
    return 1


def find_problem_folders(number: str) -> list[Path]:
    """Problem folders whose leading number token exactly matches."""
    target = number.zfill(4)
    matches = []
    for track in TRACKS:
        track_dir = ROOT / track
        if not track_dir.is_dir():
            continue
        for category in sorted(track_dir.iterdir()):
            if not category.is_dir():
                continue
            for folder in sorted(category.iterdir()):
                found = PROBLEM_FOLDER.match(folder.name)
                if folder.is_dir() and found and found.group(1) == target:
                    matches.append(folder)
    return matches


def is_solved(folder: Path) -> bool:
    """ADR-0001: Solved means at least one solution AND its notes."""
    has_solution = any((folder / name).is_file() for name in SOLUTION_FILES)
    return has_solution and (folder / "README.md").is_file()


def scan_track(track: str) -> dict[str, list[Path]]:
    """Category folder name -> sorted Solved problem folders, per track."""
    solved: dict[str, list[Path]] = {}
    track_dir = ROOT / track
    if not track_dir.is_dir():
        return solved
    for category in sorted(track_dir.iterdir()):
        if not category.is_dir():
            continue
        solved[category.name] = [
            folder
            for folder in sorted(category.iterdir())
            if folder.is_dir()
            and PROBLEM_FOLDER.match(folder.name)
            and is_solved(folder)
        ]
    return solved


def progress_table(neo: dict[str, list[Path]], general: dict[str, list[Path]]) -> str:
    rows = [
        "| Category | Progress | Status |",
        "| :--- | :---: | :--- |",
    ]
    for dirname, display, total in CURRICULUM:
        solved = len(neo.get(dirname, []))
        if solved >= total:
            status = "✅ Completed"
        elif solved > 0:
            status = "🔄 In Progress"
        else:
            status = "⏳ Not Started"
        number = dirname.split("_", 1)[0]
        rows.append(f"| {number}. {display} | {solved} / {total} | {status} |")
    general_total = sum(len(folders) for folders in general.values())
    if general_total:
        rows.append(f"| General | {general_total} | 🔄 In Progress |")
    return "\n".join(rows)


def regenerate_progress() -> int:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return fail(f"no README.md at repository root to hold the progress table")
    neo = scan_track("neetcode150")
    error = curriculum_violation(neo)
    if error:
        return fail(error)
    table = progress_table(neo, scan_track("general"))

    lines = readme.read_text().splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.strip() == PROGRESS_START]
    ends = [i for i, line in enumerate(lines) if line.strip() == PROGRESS_END]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        return fail(
            f"README.md needs exactly one {PROGRESS_START} line and one "
            f"{PROGRESS_END} line around the progress table"
        )
    rebuilt = (
        lines[: starts[0] + 1]
        + [row + "\n" for row in table.splitlines()]
        + lines[ends[0]:]
    )
    readme.write_text("".join(rebuilt))
    print(table)
    return 0


def curriculum_violation(neo: dict[str, list[Path]]) -> str | None:
    """Guard the curriculum invariant shared by progress and --list."""
    unknown = sorted(set(neo) - CURRICULUM_DIRS)
    if not unknown:
        return None
    listed = ", ".join(unknown)
    return (
        f"category folder(s) outside the curriculum constants: {listed} "
        f"(add them to CURRICULUM in run.py or move them to the general track)"
    )


def list_action() -> int:
    neo = scan_track("neetcode150")
    error = curriculum_violation(neo)
    if error:
        return fail(error)
    lines = []
    for dirname, display, _total in CURRICULUM:
        folders = neo.get(dirname, [])
        if not folders:
            continue
        number = dirname.split("_", 1)[0]
        lines.append(f"{number}. {display} ({len(folders)})")
        lines.extend(f"  {folder.name}" for folder in folders)
    general_folders = [
        folder for folders in scan_track("general").values() for folder in folders
    ]
    if general_folders:
        lines.append(f"General ({len(general_folders)})")
        lines.extend(f"  {folder.name}" for folder in general_folders)
    if lines:
        print("\n".join(lines))
    return 0


def report_exit(finished: subprocess.CompletedProcess) -> int:
    print("\n----------------------------------------")
    print(f"Process finished with exit code {finished.returncode}")
    return finished.returncode


def compile_and_run(cpp_path: Path) -> int:
    BUILD_DIR.mkdir(exist_ok=True)
    binary = BUILD_DIR / (str(cpp_path.relative_to(ROOT))
                          .replace("/", "_")
                          .replace(".cpp", ""))
    print(f"Compiling {cpp_path} ...")
    compiled = subprocess.run(
        ["g++", "-std=c++17", str(cpp_path), "-o", str(binary)]
    )
    if compiled.returncode != 0:
        return fail(f"compilation failed: {cpp_path}")
    print("Running...\n")
    return report_exit(subprocess.run([str(binary)], cwd=ROOT))


def execute_python(py_path: Path) -> int:
    print(f"Running {py_path} ...\n")
    return report_exit(subprocess.run([sys.executable, str(py_path)], cwd=ROOT))


def run_by_number(number: str, lang: str | None) -> int:
    matches = find_problem_folders(number)
    if not matches:
        return fail(
            f"no problem folder matches number '{number}' "
            f"(searched tracks: {', '.join(TRACKS)})"
        )
    if len(matches) > 1:
        listed = ", ".join(str(m.relative_to(ROOT)) for m in matches)
        return fail(f"number '{number}' matches multiple problem folders: {listed}")
    folder = matches[0]
    cpp = folder / "solution.cpp"
    py = folder / "solution.py"
    if lang is not None:
        chosen = folder / f"solution.{lang}"
        if not chosen.is_file():
            return fail(
                f"--lang {lang} given but no solution.{lang} "
                f"in {folder.relative_to(ROOT)}"
            )
        return compile_and_run(chosen) if lang == "cpp" else execute_python(chosen)
    if cpp.is_file() and py.is_file():
        return fail(
            f"number '{number}' has both languages "
            f"in {folder.relative_to(ROOT)}: solution.cpp and solution.py "
            f"— pass --lang cpp or --lang py"
        )
    if cpp.is_file():
        return compile_and_run(cpp)
    if py.is_file():
        return execute_python(py)
    return fail(f"no solution in {folder.relative_to(ROOT)}")


def run_by_path(target: str, lang: str | None) -> int:
    path = Path(target)
    if path.is_file():
        suffix = path.suffix
        if suffix not in (".cpp", ".py"):
            return fail(
                f"unsupported file type '{target}' "
                f"(only .cpp and .py are supported)"
            )
        implied = suffix.lstrip(".")
        if lang is not None and lang != implied:
            return fail(
                f"--lang {lang} does not match {suffix} file '{target}'"
            )
        path = path.resolve()
        return compile_and_run(path) if suffix == ".cpp" else execute_python(path)
    if path.exists():
        return fail(f"not a file: {target}")
    return fail(f"no such file: {target}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="Compile-and-run solutions by problem number or path.",
    )
    parser.add_argument(
        "target", nargs="?", default=None,
        help="problem number (e.g. 0217), path to a .cpp/.py file, or 'progress'",
    )
    parser.add_argument(
        "--list", dest="list_action", action="store_true",
        help="list Solved problems grouped by category",
    )
    parser.add_argument(
        "--lang", choices=("cpp", "py"),
        help="choose the language when a problem folder holds both solutions",
    )
    args = parser.parse_args(argv[1:])
    if args.list_action and args.target is not None:
        parser.error("--list cannot be combined with a target")
    if args.list_action:
        return list_action()
    if args.target is None:
        parser.error(
            "provide a problem number, a file path, or 'progress' (or pass --list)"
        )
    if args.target == "progress":
        return regenerate_progress()
    if args.target.isdigit():
        return run_by_number(args.target, args.lang)
    return run_by_path(args.target, args.lang)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
