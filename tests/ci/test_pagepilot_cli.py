import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run_pagepilot_cli(*args: str, module: str = 'pagepilot.cli') -> subprocess.CompletedProcess[str]:
	env = os.environ.copy()
	env['PYTHONPATH'] = os.pathsep.join(part for part in (str(ROOT), env.get('PYTHONPATH', '')) if part)
	return subprocess.run(
		[sys.executable, '-m', module, *args],
		cwd=ROOT,
		env=env,
		capture_output=True,
		text=True,
		timeout=20,
	)


def test_pagepilot_doctor_help_prints_pagepilot_usage():
	result = _run_pagepilot_cli('doctor', '--help')

	assert result.returncode == 0
	assert result.stdout == 'usage: pagepilot doctor [--fix-snap]\n'
	assert result.stderr == ''


def test_pagepilot_module_entrypoint_matches_cli_entrypoint():
	cli_result = _run_pagepilot_cli('doctor', '--help')
	module_result = _run_pagepilot_cli('doctor', '--help', module='pagepilot')

	assert module_result.returncode == cli_result.returncode == 0
	assert module_result.stdout == cli_result.stdout
	assert module_result.stderr == cli_result.stderr == ''


def test_normalize_captured_cli_output_handles_string_system_exit(capsys):
	from pagepilot.cli import _normalize_captured_cli_output

	def exits_with_string(_argv):
		raise SystemExit('browser-harness failed')

	assert _normalize_captured_cli_output(exits_with_string, []) == 1
	captured = capsys.readouterr()
	assert captured.out == ''
	assert captured.err == 'pagepilot failed\n'


def test_pagepilot_tui_is_deprecated_alias(monkeypatch, capsys):
	import pagepilot.cli as pagepilot_cli

	monkeypatch.setattr(pagepilot_cli, 'main', lambda: 0)

	assert pagepilot_cli.pagepilot_tui_main() == 0
	assert capsys.readouterr().err == 'pagepilot-tui is deprecated; use pagepilot instead.\n'
