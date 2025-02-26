import subprocess
import json
from collections import deque
import sys

def get_downstream_dependents(dependents_map, changed_files):
    visited = set()
    queue = deque(changed_files)

    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            for neighbor in dependents_map.get(current, []):
                queue.append(neighbor)

    return visited

def get_dependency_graph():
    res = subprocess.run(
        ["ruff", "analyze", "graph", "--direction=dependents"],
        capture_output=True,
        text=True,
    )
    return json.loads(res.stdout)


if __name__ == "__main__":
    test_dir = sys.argv[1]
    changed_files = sys.argv[2:]
    impacted_files = get_downstream_dependents(get_dependency_graph(), changed_files)
    impacted_test_files = [f for f in impacted_files if f.startswith(test_dir)]

    print(
        f"When {changed_files} changes, the downstream dependents are: {impacted_files}"
    )
    print(f"Test files that are impacted by these changes are: {impacted_test_files}")
