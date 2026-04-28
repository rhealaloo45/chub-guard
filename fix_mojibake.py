import sys

path1 = r'c:\Users\Rhea\Desktop\Tasks\chub_use_case\cli_tool\vscode-chub-guard\scripts\chub_guard.py'
path2 = r'c:\Users\Rhea\Desktop\Tasks\chub_use_case\cli_tool\scripts\chub_guard.py'

replacements = {
    'ðŸ›¡ï¸ ': '🛡️',
    'ðŸ• ': '🕒',
    'ðŸ“¦': '📦',
    'âœ¦': '✦',
    'ðŸ¤–': '🤖',
    'ðŸ“Š': '📊',
    'âš ': '⚠',
    'âœ“': '✓',
    'ðŸŸ': '🟨',
    'ðŸ”´': '🔴',
    'ðŸŸ¡': '🟡',
    'ðŸ”µ': '🔵',
    'â˜•': '☕',
    'âš™': '⚙',
    'â†’': '→',
    'â€”': '—',
}

for p in [path1, path2]:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            text = f.read()
        for bad, good in replacements.items():
            text = text.replace(bad, good)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Fixed {p}')
    except Exception as e:
        print(f'Error on {p}: {e}')
