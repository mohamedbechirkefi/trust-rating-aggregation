# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def smoke_cfg():
    return json.loads((REPO / "experiments" / "smoke.json").read_text())
