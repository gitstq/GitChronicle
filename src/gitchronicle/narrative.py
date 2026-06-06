"""
Narrative generation engine for git commit history.

Transforms structured commit data into engaging stories and changelogs.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from gitchronicle.git_parser import Commit, CommitGroup, GitParser


@dataclass
class NarrativeSection:
    """A section of the generated narrative."""
    title: str
    emoji: str
    content: str
    commits: List[Commit] = None

    def __post_init__(self):
        if self.commits is None:
            self.commits = []


class NarrativeEngine:
    """Generate narratives from git commit history."""

    # Story templates for different narrative styles
    TEMPLATES = {
        "hero": {
            "intro": "🦸 Once upon a time in the codebase...",
            "feature": "💪 Our hero added {desc}",
            "fix": "🛡️ A villainous bug was vanquished: {desc}",
            "perf": "⚡ The hero gained super speed by {desc}",
            "refactor": "🧙 The hero cast a refactoring spell: {desc}",
            "default": "✨ Something magical happened: {desc}",
        },
        "journal": {
            "intro": "📓 Developer Journal",
            "feature": "🎯 Today we built: {desc}",
            "fix": "🔧 Fixed an issue: {desc}",
            "perf": "🚀 Improved performance: {desc}",
            "refactor": "🏗️ Restructured: {desc}",
            "default": "📝 Update: {desc}",
        },
        "adventure": {
            "intro": "🗺️ The Great Coding Adventure",
            "feature": "🏰 Discovered new territory: {desc}",
            "fix": "🐉 Slayed a bug dragon: {desc}",
            "perf": "💨 Found a shortcut: {desc}",
            "refactor": "🗿 Rebuilt ancient ruins: {desc}",
            "default": "🌟 A new chapter: {desc}",
        },
    }

    def __init__(self, style: str = "journal"):
        self.style = style if style in self.TEMPLATES else "journal"
        self.template = self.TEMPLATES[self.style]

    def generate_changelog(
        self,
        commits: List[Commit],
        version: Optional[str] = None,
        title: Optional[str] = None,
    ) -> str:
        """Generate a structured changelog."""
        lines = []

        # Header
        version_str = f" [{version}]" if version else ""
        title_str = title or f"Changelog{version_str}"
        lines.append(f"# {title_str}")
        lines.append("")

        # Date range
        if commits:
            first_date = min(c.date for c in commits)
            last_date = max(c.date for c in commits)
            lines.append(f"📅 **Period:** {first_date.strftime('%Y-%m-%d')} ~ {last_date.strftime('%Y-%m-%d')}")
            lines.append("")

        # Group commits by category
        groups = self._group_by_category(commits)

        for group in groups:
            if not group.commits:
                continue
            lines.append(f"## {group.title}")
            lines.append("")
            for commit in group.commits:
                breaking = " 💥 **BREAKING**" if commit.is_breaking else ""
                scope = f"**[{commit.scope}]** " if commit.scope else ""
                lines.append(
                    f"- {scope}{commit.subject}{breaking} "
                    f"(`{commit.short_hash}` by @{commit.author})"
                )
            lines.append("")

        # Statistics
        stats = self._generate_stats(commits)
        if stats:
            lines.append("## 📊 Statistics")
            lines.append("")
            lines.append(stats)
            lines.append("")

        return "\n".join(lines)

    def generate_story(
        self,
        commits: List[Commit],
        title: Optional[str] = None,
    ) -> str:
        """Generate an engaging story from commits."""
        lines = []

        # Title
        story_title = title or self.template["intro"]
        lines.append(f"# {story_title}")
        lines.append("")

        if not commits:
            lines.append("*No commits to tell a story about...*")
            return "\n".join(lines)

        # Introduction
        first_date = min(c.date for c in commits)
        last_date = max(c.date for c in commits)
        days = (last_date - first_date).days + 1

        lines.append(
            f"This tale spans **{days} day{'s' if days > 1 else ''}** "
            f"({first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}), "
            f"featuring **{len(commits)} commits** by **{len(set(c.author for c in commits))} brave developers**.")
        lines.append("")

        # Group by time periods (days or weeks)
        periods = self._group_by_period(commits)

        for period_name, period_commits in periods.items():
            lines.append(f"## 📅 {period_name}")
            lines.append("")

            # Sort by significance (breaking changes first, then by category)
            sorted_commits = sorted(
                period_commits,
                key=lambda c: (
                    not c.is_breaking,
                    c.category != "✨ Features",
                    c.category != "🐛 Bug Fixes",
                    c.date,
                )
            )

            for commit in sorted_commits:
                story_line = self._commit_to_story_line(commit)
                lines.append(f"- {story_line}")

            lines.append("")

        # Conclusion
        lines.append("## 🎉 The End... For Now")
        lines.append("")
        lines.append(
            "And so, the codebase continues to evolve, "
            "with each commit adding a new verse to this never-ending story. 🚀"
        )

        return "\n".join(lines)

    def generate_release_notes(
        self,
        commits: List[Commit],
        version: str,
        compare_url: Optional[str] = None,
    ) -> str:
        """Generate release notes."""
        lines = []

        lines.append(f"# 🚀 Release {version}")
        lines.append("")

        # Highlights
        breaking = [c for c in commits if c.is_breaking]
        features = [c for c in commits if c.category == "✨ Features"]
        fixes = [c for c in commits if c.category == "🐛 Bug Fixes"]

        if breaking:
            lines.append("## 💥 Breaking Changes")
            lines.append("")
            for c in breaking:
                lines.append(f"- {c.subject} (`{c.short_hash}`)")
            lines.append("")

        if features:
            lines.append("## ✨ New Features")
            lines.append("")
            for c in features[:10]:  # Top 10
                lines.append(f"- {c.subject} (`{c.short_hash}`)")
            if len(features) > 10:
                lines.append(f"- ... and {len(features) - 10} more features")
            lines.append("")

        if fixes:
            lines.append("## 🐛 Bug Fixes")
            lines.append("")
            for c in fixes[:10]:
                lines.append(f"- {c.subject} (`{c.short_hash}`)")
            if len(fixes) > 10:
                lines.append(f"- ... and {len(fixes) - 10} more fixes")
            lines.append("")

        # Full changelog link
        if compare_url:
            lines.append(f"📋 [Full Changelog]({compare_url})")
            lines.append("")

        # Contributors
        contributors = sorted(set(c.author for c in commits))
        if contributors:
            lines.append("## 👏 Contributors")
            lines.append("")
            for author in contributors:
                count = sum(1 for c in commits if c.author == author)
                lines.append(f"- @{author} ({count} commits)")
            lines.append("")

        return "\n".join(lines)

    def _group_by_category(self, commits: List[Commit]) -> List[CommitGroup]:
        """Group commits by category."""
        groups: Dict[str, List[Commit]] = {}
        for commit in commits:
            cat = commit.category
            if cat not in groups:
                groups[cat] = []
            groups[cat].append(commit)

        # Sort categories by priority
        priority_order = [
            "💥 Breaking Changes",
            "✨ Features",
            "🐛 Bug Fixes",
            "⚡ Performance",
            "♻️ Refactoring",
            "📚 Documentation",
            "🧪 Tests",
            "📦 Build",
            "👷 CI/CD",
            "🔧 Chores",
            "💎 Styles",
            "⏪ Reverts",
            "🔧 Other",
        ]

        result = []
        for cat in priority_order:
            if cat in groups:
                result.append(CommitGroup(
                    title=cat,
                    commits=sorted(groups[cat], key=lambda c: c.date, reverse=True)
                ))

        # Add any remaining categories
        for cat, cat_commits in groups.items():
            if cat not in priority_order:
                result.append(CommitGroup(
                    title=cat,
                    commits=sorted(cat_commits, key=lambda c: c.date, reverse=True)
                ))

        return result

    def _group_by_period(
        self,
        commits: List[Commit],
    ) -> Dict[str, List[Commit]]:
        """Group commits by time period."""
        periods: Dict[str, List[Commit]] = {}

        for commit in commits:
            # Use week as period
            year, week, _ = commit.date.isocalendar()
            period_key = f"Week {week}, {year}"

            if period_key not in periods:
                periods[period_key] = []
            periods[period_key].append(commit)

        # Sort by date
        return dict(sorted(periods.items(), key=lambda x: min(c.date for c in x[1])))

    def _commit_to_story_line(self, commit: Commit) -> str:
        """Convert a commit to a story line."""
        desc = commit.subject

        if commit.is_breaking:
            return f"💥 **MAJOR EVENT!** {desc}"
        elif commit.category == "✨ Features":
            return self.template["feature"].format(desc=desc)
        elif commit.category == "🐛 Bug Fixes":
            return self.template["fix"].format(desc=desc)
        elif commit.category == "⚡ Performance":
            return self.template["perf"].format(desc=desc)
        elif commit.category == "♻️ Refactoring":
            return self.template["refactor"].format(desc=desc)
        else:
            return self.template["default"].format(desc=desc)

    def _generate_stats(self, commits: List[Commit]) -> str:
        """Generate statistics markdown."""
        if not commits:
            return ""

        authors = {}
        categories = {}
        for c in commits:
            authors[c.author] = authors.get(c.author, 0) + 1
            categories[c.category] = categories.get(c.category, 0) + 1

        lines = []
        lines.append(f"- **Total Commits:** {len(commits)}")
        lines.append(f"- **Contributors:** {len(authors)}")
        lines.append(f"- **Categories:** {len(categories)}")
        lines.append("")
        lines.append("**By Category:**")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            lines.append(f"  - {cat}: {count}")

        return "\n".join(lines)
