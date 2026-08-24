"""Black-box tests for the Runner, at the CLI seam.

The Runner under test is a copy of the repository's runner script placed at the
root of a fixture tree (a fabricated tracks/categories/problems layout in a
temporary directory). Tests invoke it as a subprocess and assert on stdout,
exit codes, and filesystem effects. Runner internals are never imported.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNNER_SOURCE = REPO_ROOT / "run.py"

CPP_HELLO = """\
#include <iostream>
int main() {
    std::cout << "fixture output" << std::endl;
    return 0;
}
"""


CPP_FAILING = """\
#include <iostream>
int main() {
    std::cout << "fixture output" << std::endl;
    return 3;
}
"""


PY_HELLO = "print('py fixture output')\n"
PY_EXITING = "import sys\nprint('py fixture output')\nsys.exit(3)\n"
PY_RAISING = "raise ValueError('boom')\n"




class RunnerCliTestCase(unittest.TestCase):
    """Fixture tree + subprocess harness around the runner script."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.runner = self.root / "run.py"
        shutil.copy2(RUNNER_SOURCE, self.runner)

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.runner), *args],
            capture_output=True,
            text=True,
            cwd=self.root,
        )

    def add_problem(self, number, name, category="01_arrays_hashing",
                    track="neetcode150", files=None):
        folder = self.root / track / category / f"{number}_{name}"
        folder.mkdir(parents=True, exist_ok=True)
        for fname, content in (files or {}).items():
            (folder / fname).write_text(content)
        return folder


class TestPathMode(RunnerCliTestCase):
    def test_runs_cpp_file_by_path_and_exits_zero(self):
        folder = self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        result = self.run_cli(str(folder / "solution.cpp"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fixture output", result.stdout)

    def test_no_argument_prints_usage_and_fails(self):
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage", (result.stdout + result.stderr).lower())

    def test_nonexistent_path_fails_naming_the_target(self):
        result = self.run_cli("nope.cpp")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nope.cpp", result.stderr)


class TestNumberMode(RunnerCliTestCase):
    def test_runs_solution_by_exact_number(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        result = self.run_cli("0217")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fixture output", result.stdout)

    def test_short_number_is_zero_padded_to_match(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        result = self.run_cli("217")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fixture output", result.stdout)

    def test_runs_solution_from_general_track(self):
        self.add_problem(
            "0999", "some_problem", track="general",
            files={"solution.cpp": CPP_HELLO},
        )
        result = self.run_cli("0999")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fixture output", result.stdout)


class TestNumberResolutionErrors(RunnerCliTestCase):
    def test_prefix_number_does_not_match_longer_folder(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        result = self.run_cli("021")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("021", result.stderr)
        self.assertIn("no problem folder matches", result.stderr)

    def test_colliding_numbers_error_names_both_folders(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        self.add_problem(
            "0217", "duplicate_number", category="02_two_pointers",
            files={"solution.cpp": CPP_HELLO},
        )
        result = self.run_cli("0217")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("0217_contains_duplicate", result.stderr)
        self.assertIn("0217_duplicate_number", result.stderr)

    def test_number_without_any_solution_fails_naming_folder(self):
        self.add_problem("0217", "contains_duplicate", files={"README.md": "notes"})
        result = self.run_cli("0217")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no solution", result.stderr)
        self.assertIn("0217_contains_duplicate", result.stderr)


class TestCompileFailure(RunnerCliTestCase):
    def test_compile_failure_names_file_and_shows_compiler_output(self):
        folder = self.add_problem(
            "0217", "contains_duplicate",
            files={"solution.cpp": "int main() { this is not c++ }"},
        )
        result = self.run_cli(str(folder / "solution.cpp"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compilation failed", result.stderr)
        self.assertIn("solution.cpp", result.stderr)
        self.assertIn("error", (result.stdout + result.stderr).lower())


class TestExecutionSemantics(RunnerCliTestCase):
    def test_solution_exit_code_propagates(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_FAILING}
        )
        result = self.run_cli("0217")
        self.assertEqual(result.returncode, 3, result.stderr)

    def test_build_artifacts_confined_to_build_dir(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        before = {p.name for p in self.root.iterdir()}
        result = self.run_cli("0217")
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {p.name for p in self.root.iterdir()}
        self.assertEqual(after - before - {".build"}, set())
        binaries = list((self.root / ".build").iterdir())
        self.assertEqual(len(binaries), 1, binaries)
        self.assertIn("0217", binaries[0].name)



class TestPythonDispatch(RunnerCliTestCase):
    def test_runs_python_solution_by_number(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.py": PY_HELLO}
        )
        result = self.run_cli("0217")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("py fixture output", result.stdout)

    def test_runs_python_file_by_path(self):
        folder = self.add_problem(
            "0217", "contains_duplicate", files={"visual.py": PY_HELLO}
        )
        result = self.run_cli(str(folder / "visual.py"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("py fixture output", result.stdout)

    def test_python_exit_code_propagates(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.py": PY_EXITING}
        )
        result = self.run_cli("0217")
        self.assertEqual(result.returncode, 3, result.stderr)

    def test_python_traceback_is_surfaced_not_swallowed(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.py": PY_RAISING}
        )
        result = self.run_cli("0217")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Traceback", result.stderr)
        self.assertIn("ValueError", result.stderr)


class TestLanguageCoexistence(RunnerCliTestCase):
    BOTH = {"solution.cpp": CPP_HELLO, "solution.py": PY_HELLO}

    def test_both_solutions_without_lang_error_names_both_files(self):
        self.add_problem("0217", "contains_duplicate", files=self.BOTH)
        result = self.run_cli("0217")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("solution.cpp", result.stderr)
        self.assertIn("solution.py", result.stderr)
        self.assertIn("--lang", result.stderr)

    def test_lang_cpp_selects_exactly_the_cpp_solution(self):
        self.add_problem("0217", "contains_duplicate", files=self.BOTH)
        result = self.run_cli("--lang", "cpp", "0217")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fixture output", result.stdout)
        self.assertNotIn("py fixture output", result.stdout)

    def test_lang_py_selects_exactly_the_python_solution(self):
        self.add_problem("0217", "contains_duplicate", files=self.BOTH)
        result = self.run_cli("--lang", "py", "0217")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("py fixture output", result.stdout)
        self.assertNotIn("Compiling", result.stdout)

    def test_lang_choice_without_that_solution_fails_naming_folder(self):
        self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        result = self.run_cli("--lang", "py", "0217")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("solution.py", result.stderr)
        self.assertIn("0217_contains_duplicate", result.stderr)

    def test_lang_conflicting_with_path_extension_fails(self):
        folder = self.add_problem(
            "0217", "contains_duplicate", files={"solution.cpp": CPP_HELLO}
        )
        result = self.run_cli("--lang", "py", str(folder / "solution.cpp"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match", result.stderr)


README_WITH_MARKERS = """\
# Fixture repo

Intro prose that must survive every regeneration.

<!-- progress:start -->
stale hand-written table
<!-- progress:end -->

Trailing prose that must also survive.
"""


class TestProgress(RunnerCliTestCase):
    def write_readme(self):
        readme = self.root / "README.md"
        readme.write_text(README_WITH_MARKERS)
        return readme

    def read_between_markers(self, readme):
        content = readme.read_text()
        _, _, between = content.partition("<!-- progress:start -->")
        between, _, _ = between.partition("<!-- progress:end -->")
        return between

    def test_progress_writes_solved_count_between_markers(self):
        self.add_problem(
            "0001", "two_sum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        self.add_problem("0036", "valid_sudoku", files={"solution.cpp": CPP_HELLO})
        readme = self.write_readme()

        result = self.run_cli("progress")

        self.assertEqual(result.returncode, 0, result.stderr)
        content = readme.read_text()
        self.assertIn("| 01. Arrays & Hashing | 1 / 9 |", content)
        self.assertNotIn("2 / 9", content)
        self.assertNotIn("stale hand-written table", content)

    def test_progress_preserves_prose_outside_markers(self):
        self.add_problem(
            "0001", "two_sum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        readme = self.write_readme()

        result = self.run_cli("progress")

        self.assertEqual(result.returncode, 0, result.stderr)
        content = readme.read_text()
        self.assertTrue(content.startswith("# Fixture repo\n"), content)
        self.assertIn("Intro prose that must survive every regeneration.", content)
        self.assertIn("Trailing prose that must also survive.", content)
        self.assertIn("<!-- progress:start -->", content)
        self.assertIn("<!-- progress:end -->", content)

    def test_regenerating_twice_is_byte_identical(self):
        self.add_problem(
            "0001", "two_sum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        readme = self.write_readme()
        first = self.run_cli("progress")
        self.assertEqual(first.returncode, 0, first.stderr)
        once = readme.read_bytes()

        second = self.run_cli("progress")

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(readme.read_bytes(), once)


    def test_all_categories_appear_in_curriculum_order_with_zeros(self):
        self.add_problem(
            "0207", "course_schedule", category="11_graphs",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        readme = self.write_readme()

        result = self.run_cli("progress")

        self.assertEqual(result.returncode, 0, result.stderr)
        labels = [
            line.split("|")[1].strip()
            for line in self.read_between_markers(readme).splitlines()
            if line.startswith("|") and "Category" not in line and ":---" not in line
        ]
        expected = [
            "01. Arrays & Hashing", "02. Two Pointers", "03. Sliding Window",
            "04. Stack", "05. Binary Search", "06. Linked List", "07. Trees",
            "08. Tries", "09. Heap / Priority Queue", "10. Backtracking",
            "11. Graphs", "12. Advanced Graphs", "13. 1D Dynamic Programming",
            "14. 2D Dynamic Programming", "15. Greedy", "16. Intervals",
            "17. Math & Geometry", "18. Bit Manipulation",
        ]
        self.assertEqual(labels[:18], expected)
        content = readme.read_text()
        self.assertIn("| 11. Graphs | 1 / 13 |", content)
        self.assertIn("| 08. Tries | 0 / 3 |", content)

    def test_general_track_row_counts_solved_without_denominator(self):
        self.add_problem(
            "0999", "off_roadmap", track="general",
            files={"solution.py": PY_HELLO, "README.md": "notes"},
        )
        self.add_problem(
            "1000", "notes_missing", track="general",
            files={"solution.py": PY_HELLO},
        )
        readme = self.write_readme()

        result = self.run_cli("progress")

        self.assertEqual(result.returncode, 0, result.stderr)
        content = readme.read_text()
        self.assertIn("| General | 1 |", content)
        self.assertNotIn("| General | 2 |", content)

    def test_general_track_row_absent_when_track_missing(self):
        self.add_problem(
            "0001", "two_sum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        readme = self.write_readme()

        result = self.run_cli("progress")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("General", readme.read_text())

    def test_missing_markers_fail_and_leave_readme_untouched(self):
        readme = self.root / "README.md"
        original = "# Fixture repo\n\nNo markers here at all.\n"
        readme.write_text(original)

        result = self.run_cli("progress")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("progress:start", result.stderr)
        self.assertEqual(readme.read_text(), original)

    def test_category_outside_curriculum_constants_fails_naming_it(self):
        self.add_problem(
            "0001", "two_sum", category="19_beyond_curriculum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        readme = self.write_readme()

        result = self.run_cli("progress")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("19_beyond_curriculum", result.stderr)
        self.assertEqual(readme.read_text(), README_WITH_MARKERS)

    def test_readme_missing_entirely_fails_without_creating_it(self):
        result = self.run_cli("progress")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("README.md", result.stderr)
        self.assertFalse((self.root / "README.md").exists())


class TestListAction(RunnerCliTestCase):
    def test_lists_solved_grouped_by_category_in_curriculum_order(self):
        self.add_problem(
            "0207", "course_schedule", category="11_graphs",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        self.add_problem(
            "0001", "two_sum",
            files={"solution.py": PY_HELLO, "README.md": "notes"},
        )
        self.add_problem("0036", "valid_sudoku", files={"solution.cpp": CPP_HELLO})

        result = self.run_cli("--list")

        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(lines[0], "01. Arrays & Hashing (1)")
        self.assertEqual(lines[1], "  0001_two_sum")
        self.assertEqual(lines[2], "11. Graphs (1)")
        self.assertEqual(lines[3], "  0207_course_schedule")
        self.assertNotIn("0036_valid_sudoku", result.stdout)

    def test_category_header_only_when_it_has_solved_problems(self):
        self.add_problem(
            "0001", "two_sum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )

        result = self.run_cli("--list")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("01. Arrays & Hashing (1)", result.stdout)
        self.assertNotIn("Two Pointers", result.stdout)
        self.assertNotIn("Bit Manipulation", result.stdout)

    def test_list_counts_agree_with_progress_table(self):
        self.add_problem(
            "0001", "two_sum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )
        self.add_problem(
            "0242", "valid_anagram",
            files={"solution.py": PY_HELLO, "README.md": "notes"},
        )
        self.add_problem("0036", "valid_sudoku", files={"solution.cpp": CPP_HELLO})
        self.add_problem(
            "0999", "off_roadmap", track="general",
            files={"solution.py": PY_HELLO, "README.md": "notes"},
        )
        readme = self.root / "README.md"
        readme.write_text(README_WITH_MARKERS)

        listing = self.run_cli("--list")
        table = self.run_cli("progress")

        self.assertEqual(listing.returncode, 0, listing.stderr)
        self.assertEqual(table.returncode, 0, table.stderr)
        listed = {}
        for line in listing.stdout.splitlines():
            if line and not line.startswith(" "):
                name, _, count = line.rpartition(" (")
                listed[name] = int(count.rstrip(")"))
        rows = {
            parts[0].strip(): int(parts[1].strip().split(" / ")[0])
            for parts in (
                row.strip().strip("|").split("|")
                for row in readme.read_text().splitlines()
                if row.startswith("|") and "Category" not in row and ":---" not in row
            )
        }
        for name, count in listed.items():
            self.assertEqual(rows[name], count, f"{name} disagrees")
        self.assertEqual(listed["01. Arrays & Hashing"], 2)
        self.assertEqual(listed["General"], 1)

    def test_empty_tree_lists_nothing_and_exits_zero(self):
        result = self.run_cli("--list")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_list_fails_on_category_outside_curriculum_constants(self):
        self.add_problem(
            "0001", "two_sum", category="19_beyond_curriculum",
            files={"solution.cpp": CPP_HELLO, "README.md": "notes"},
        )

        result = self.run_cli("--list")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("19_beyond_curriculum", result.stderr)

    def test_list_cannot_be_combined_with_a_target(self):
        result = self.run_cli("--list", "0217")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage", (result.stdout + result.stderr).lower())
if __name__ == "__main__":
    unittest.main()
