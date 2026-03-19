import importlib.resources
import subprocess
import pytest
import sys

import linkcheckmd as lc


def test_local():
    resource = importlib.resources.files("linkcheckmd.tests") / "badlink.md"
    with importlib.resources.as_file(resource) as file:
        urls = list(lc.check_local(file, ext=".md"))
    assert len(urls) == 2


@pytest.mark.parametrize("use_async", [True, False])
def test_mod(use_async):
    if not use_async:
        pytest.importorskip("requests", reason="Synchronous requires requests")
    resource = importlib.resources.files("linkcheckmd.tests") / "badlink.md"
    with importlib.resources.as_file(resource) as file:
        urls = lc.check_remotes(
            file, domain="github.invalid", ext=".md", use_async=use_async
        )
    assert len(urls) == 2


@pytest.mark.parametrize("use_async", [True, False])
def test_script(use_async, capfd):
    args = []
    if not use_async:
        pytest.importorskip("requests", reason="Synchronous requires requests")
        args.append("--sync")
    resource = importlib.resources.files("linkcheckmd.tests") / "badlink.md"
    with importlib.resources.as_file(resource) as file:
        ret = subprocess.run(
            [sys.executable, "-m", "linkcheckmd", str(file), "github.invalid"] + args,
            text=True,
        )
    assert ret.returncode == 22
    assert "github.invalid" in capfd.readouterr().out
