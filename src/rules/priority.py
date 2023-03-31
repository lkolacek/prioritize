import jira

PRIORITY = [
    "Undefined",
    "Minor",
    "Normal",
    "Major",
    "Critical",
    "Blocker",
]


def _get_max_priority(issues: list[jira.resources.Issue]) -> str:
    priority_ids = [PRIORITY.index(i.fields.priority.name) for i in issues]
    if priority_ids:
        max_priority = max(priority_ids)
    else:
        max_priority = 0
    return PRIORITY[max_priority]


def check_priority(issue: jira.resources.Issue, context: dict, dry_run: bool) -> None:
    related_issues = list(issue.raw["Related Issues"]["Blocks"])
    parent_issue = issue.raw["Related Issues"]["Parent"]
    if parent_issue is not None:
        related_issues.append(parent_issue)
    target_priority = _get_max_priority(related_issues)
    if issue.fields.priority.name != target_priority:
        context["updates"].append(
            f"  > Issue priority set to '{target_priority}' (was '{issue.fields.priority.name}')."
        )
    if not dry_run:
        issue.update(priority={"name": target_priority})
