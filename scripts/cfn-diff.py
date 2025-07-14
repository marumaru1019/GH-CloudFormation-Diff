#!/usr/bin/env python3
import sys
import subprocess
import yaml
from deepdiff import DeepDiff

def load_version(file_path: str, ref: str):
    """
    指定リファレンス(ref)のコミットからファイルを取得し、YAML をパースして返す
    """
    content = subprocess.check_output(
        ['git', 'show', f'{ref}:{file_path}']
    )
    return yaml.safe_load(content)

def summarize_diff(old: dict, new: dict):
    """
    DeepDiff で検出した出力を読みやすい文字列に整形する
    """
    diff = DeepDiff(old, new, ignore_order=True)
    lines = []
    # 変更されたプロパティを列挙
    for change_type, changes in diff.items():
        for path, detail in changes.items():
            old_val = detail.get('old_value', '<absent>')
            new_val = detail.get('new_value', '<absent>')
            lines.append(f"- `{path}`: `{old_val}` → `{new_val}`")
    return lines

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: cfn_diff.py <base_ref> <head_ref>', file=sys.stderr)
        sys.exit(1)

    base_ref, head_ref = sys.argv[1], sys.argv[2]
    try:
        with open('changed_templates.txt') as f:
            files = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print('No changed_templates.txt found.', file=sys.stderr)
        sys.exit(1)

    output_lines = []
    for tpl in files:
        output_lines.append(f"### Diff in `{tpl}`")
        try:
            old = load_version(tpl, base_ref) or {}
            new = load_version(tpl, head_ref) or {}
            for line in summarize_diff(old, new):
                output_lines.append(line)
        except subprocess.CalledProcessError:
            output_lines.append(f"- Could not load `{tpl}` at one of the refs.")
        output_lines.append('')

    # コメント用にまとめて出力
    print('\n'.join(output_lines))