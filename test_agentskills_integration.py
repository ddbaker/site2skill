import os
import shutil
import subprocess
import sys
import tempfile

import pytest

from site2skill.generate_skill_structure import generate_skill_structure


def test_agentskills_validate_generated_skill():
    pytest.importorskip("skills_ref")

    fixture_dir = os.path.join(
        os.path.dirname(__file__),
        "tests",
        "fixtures",
        "site2skill",
        "markdown",
    )

    temp_dir = tempfile.mkdtemp()
    try:
        output_base = os.path.join(temp_dir, "skills")
        generate_skill_structure("example-skill", fixture_dir, output_base)
        skill_dir = os.path.join(output_base, "example-skill")

        result = subprocess.run(
            [sys.executable, "-m", "skills_ref.cli", "validate", skill_dir],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    finally:
        shutil.rmtree(temp_dir)
