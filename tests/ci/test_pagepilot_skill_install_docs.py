import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGEPILOT_REPO_SKILL_URL = 'https://raw.githubusercontent.com/pagepilot/pagepilot/main/skills/pagepilot/SKILL.md'
EXPECTED_SKILL_INSTALL_PATHS = (
	Path('.agents') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.claude') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.codex') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.copilot') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.cursor') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.gemini') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.openclaw') / 'skills' / 'pagepilot' / 'SKILL.md',
	Path('.config') / 'opencode' / 'skills' / 'pagepilot' / 'SKILL.md',
)


def _fake_browser_harness_tools(tmp_path: Path, skill_text: str) -> Path:
	bin_dir = tmp_path / 'bin'
	bin_dir.mkdir()

	uv = bin_dir / 'uv'
	uv.write_text(
		'#!/usr/bin/env python3\n'
		'import os, pathlib, sys\n'
		'pathlib.Path(os.environ["UV_TOOL_INSTALL_ARGS_FILE"]).write_text(" ".join(sys.argv[1:]), encoding="utf-8")\n',
		encoding='utf-8',
	)
	uv.chmod(0o755)

	browser_harness = bin_dir / 'browser-harness'
	browser_harness.write_text(
		'#!/usr/bin/env python3\n'
		'import sys\n'
		f'text = {skill_text!r}\n'
		'if sys.argv[1:] == ["skill"]:\n'
		'    print(text, end="")\n'
		'else:\n'
		'    print("usage: browser-harness skill", file=sys.stderr)\n'
		'    sys.exit(2)\n',
		encoding='utf-8',
	)
	browser_harness.chmod(0o755)
	return bin_dir


def test_docs_install_pagepilot_skill_from_package_alias():
	readme = (ROOT / 'README.md').read_text(encoding='utf-8')

	assert 'run `pagepilot skill install` to register the skill' in readme
	assert 'mkdir -p ~/.claude/skills/pagepilot' not in readme
	assert 'uv run --with "pagepilot[browser-harness]" python -c' not in readme
	assert 'from pagepilot.skills import pagepilot_skill_text' not in readme
	assert PAGEPILOT_REPO_SKILL_URL not in readme
	assert 'raw.githubusercontent.com/pagepilot/browser-harness/main/SKILL.md' not in readme


def test_cloud_v4_reference_scopes_workspace_file_listing():
	api_v4 = (ROOT / 'skills' / 'cloud' / 'references' / 'api-v4.md').read_text(encoding='utf-8')

	assert 'client.workspaces.files(workspace.id)' in api_v4
	assert 'client.workspaces.files()' not in api_v4
	python_examples = re.findall(r'```python\n(.*?)```', api_v4, flags=re.DOTALL)
	assert python_examples
	assert all('PagePilot' in example for example in python_examples if 'client.' in example)


def test_remote_browser_skill_uses_current_cli():
	remote_skill = (ROOT / 'skills' / 'remote-browser' / 'SKILL.md').read_text(encoding='utf-8')

	for removed_command in (
		'pagepilot open',
		'pagepilot state',
		'pagepilot click',
		'pagepilot input',
		'pagepilot tab',
		'pagepilot screenshot',
		'pagepilot eval',
		'pagepilot cookies',
		'pagepilot close',
		'pagepilot sessions',
		'pagepilot tunnel',
		'pagepilot wait',
		'pagepilot register',
		'pagepilot cloud connect',
		'pagepilot --connect',
		'pagepilot/skill_cli/README.md',
	):
		assert removed_command not in remote_skill

	for current_command in (
		"pagepilot <<'PY'",
		'start_remote_daemon("r7k2")',
		'BU_NAME=r7k2 pagepilot',
		'new_tab("https://example.com")',
		'print(page_info())',
		'stop_remote_daemon("r7k2")',
	):
		assert current_command in remote_skill


def test_pagepilot_cli_installs_browser_harness_package_skill(tmp_path):
	bin_dir = _fake_browser_harness_tools(tmp_path, '---\nname: browser-harness\n---\n\n# Browser Harness\n')

	home = tmp_path / 'home'
	for stale in (home / path for path in EXPECTED_SKILL_INSTALL_PATHS):
		stale.parent.mkdir(parents=True)
		stale.write_text('stale pagepilot skill', encoding='utf-8')

	uv_args = tmp_path / 'uv-args.txt'
	env = os.environ.copy()
	env['HOME'] = str(home)
	env['PATH'] = os.pathsep.join(part for part in (str(bin_dir), env.get('PATH', '')) if part)
	env['PYTHONPATH'] = os.pathsep.join(part for part in (str(ROOT), env.get('PYTHONPATH', '')) if part)
	env['UV_TOOL_INSTALL_ARGS_FILE'] = str(uv_args)

	result = subprocess.run(
		[sys.executable, '-m', 'pagepilot.cli', 'skill', 'install'],
		cwd=ROOT,
		env=env,
		capture_output=True,
		text=True,
		timeout=10,
	)

	assert result.returncode == 0, result.stderr
	assert uv_args.read_text(encoding='utf-8') == 'tool install --python 3.12 --upgrade --force pagepilot'
	expected = (
		'---\n'
		'name: pagepilot\n'
		'description: "Direct browser control via CDP for web interaction: automation, scraping, testing, screenshots, and site/app work."\n'
		'homepage: https://pagepilot.com\n'
		'metadata:\n'
		'  {\n'
		'    "openclaw":\n'
		'      {\n'
		'        "requires": { "bins": ["pagepilot"] },\n'
		'        "install":\n'
		'          [\n'
		'            {\n'
		'              "id": "uv",\n'
		'              "kind": "uv",\n'
		'              "package": "pagepilot",\n'
		'              "bins": ["pagepilot"],\n'
		'              "label": "Install Browser Use CLI (uv)",\n'
		'            },\n'
		'          ],\n'
		'      },\n'
		'  }\n'
		'---\n\n'
		'# Browser Use\n'
	)
	for installed in (home / path for path in EXPECTED_SKILL_INSTALL_PATHS):
		assert installed.read_text(encoding='utf-8') == expected


def test_pagepilot_cli_validates_destination_before_installing_harness(tmp_path):
	bin_dir = _fake_browser_harness_tools(tmp_path, '---\nname: browser-harness\n---\n\n# Browser Harness\n')
	blocking_file = tmp_path / 'not-a-directory'
	blocking_file.write_text('blocks skill directory creation', encoding='utf-8')

	uv_args = tmp_path / 'uv-args.txt'
	env = os.environ.copy()
	env['HOME'] = str(tmp_path / 'home')
	env['PATH'] = os.pathsep.join(part for part in (str(bin_dir), env.get('PATH', '')) if part)
	env['PYTHONPATH'] = os.pathsep.join(part for part in (str(ROOT), env.get('PYTHONPATH', '')) if part)
	env['UV_TOOL_INSTALL_ARGS_FILE'] = str(uv_args)

	result = subprocess.run(
		[sys.executable, '-m', 'pagepilot.cli', 'skill', 'install', '--path', str(blocking_file / 'nested')],
		cwd=ROOT,
		env=env,
		capture_output=True,
		text=True,
		timeout=10,
	)

	assert result.returncode == 1
	assert 'is not a directory' in result.stderr
	assert not uv_args.exists()
