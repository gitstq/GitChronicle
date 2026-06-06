"""
Git commit history parser and analyzer.

Extracts, categorizes, and enriches git commit data for narrative generation.
"""

import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Commit:
    """Represents a single git commit."""
    hash: str
    short_hash: str
    author: str
    email: str
    date: datetime
    message: str
    subject: str = ""
    body: str = ""
    files_changed: List[str] = field(default_factory=list)
    insertions: int = 0
    deletions: int = 0
    tags: List[str] = field(default_factory=list)
    category: str = "other"
    is_breaking: bool = False
    scope: str = ""


@dataclass
class CommitGroup:
    """A group of related commits (e.g., by category or time period)."""
    title: str
    commits: List[Commit] = field(default_factory=list)
    summary: str = ""


class GitParser:
    """Parse git repository commit history."""

    # Conventional commit categories
    CATEGORIES = {
        "feat": "✨ Features",
        "fix": "🐛 Bug Fixes",
        "docs": "📚 Documentation",
        "style": "💎 Styles",
        "refactor": "♻️ Refactoring",
        "perf": "⚡ Performance",
        "test": "🧪 Tests",
        "chore": "🔧 Chores",
        "ci": "👷 CI/CD",
        "build": "📦 Build",
        "revert": "⏪ Reverts",
    }

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def _run_git(self, args: List[str]) -> str:
        """Execute a git command and return output."""
        cmd = ["git", "-C", self.repo_path] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if result.returncode != 0:
            raise GitChronicleError(f"Git command failed: {result.stderr}")
        return result.stdout

    def get_commits(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
        author: Optional[str] = None,
        max_count: Optional[int] = None,
        branch: str = "HEAD"
    ) -> List[Commit]:
        """Extract commits from git history."""
        format_str = (
            "%H%x00%h%x00%an%x00%ae%x00%ad%x00%s%x00%b%x00"
            "--FILES--%x00"
        )

        args = [
            "log",
            branch,
            f"--format={format_str}",
            "--date=iso-strict",
            "--name-status",
        ]

        if since:
            args.extend(["--since", since])
        if until:
            args.extend(["--until", until])
        if author:
            args.extend(["--author", author])
        if max_count:
            args.extend(["-n", str(max_count)])

        output = self._run_git(args)
        return self._parse_log_output(output)

    def _parse_log_output(self, output: str) -> List[Commit]:
        """Parse git log output into Commit objects."""
        commits = []
        entries = output.split("\n--FILES--\n")

        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            parts = entry.split("\x00")
            if len(parts) < 6:
                continue

            commit = self._create_commit(parts)
            commits.append(commit)

        return commits

    def _create_commit(self, parts: List[str]) -> Commit:
        """Create a Commit object from parsed parts."""
        hash_val = parts[0]
        short_hash = parts[1] if len(parts) > 1 else hash_val[:7]
        author = parts[2] if len(parts) > 2 else "Unknown"
        email = parts[3] if len(parts) > 3 else ""
        date_str = parts[4] if len(parts) > 4 else ""
        subject = parts[5] if len(parts) > 5 else ""
        body = parts[6] if len(parts) > 6 else ""

        # Parse files from remaining parts
        files = []
        remaining = "\x00".join(parts[7:]) if len(parts) > 7 else ""
        for line in remaining.split("\n"):
            line = line.strip()
            if line and not line.startswith("-"):
                parts_file = line.split("\t")
                if len(parts_file) >= 2:
                    files.append(parts_file[-1])

        # Parse date
        try:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            date = datetime.now()

        # Categorize commit
        category, scope, is_breaking = self._categorize_commit(subject)

        return Commit(
            hash=hash_val,
            short_hash=short_hash,
            author=author,
            email=email,
            date=date,
            message=f"{subject}\n\n{body}".strip(),
            subject=subject,
            body=body,
            files_changed=files,
            category=category,
            is_breaking=is_breaking,
            scope=scope,
        )

    def _categorize_commit(self, subject: str) -> tuple:
        """Categorize a commit based on conventional commit format."""
        pattern = r"^(\w+)(?:\(([^)]+)\))?!?:\s*(.+)$"
        match = re.match(pattern, subject)

        if match:
            cat_key = match.group(1).lower()
            scope = match.group(2) or ""
            message = match.group(3)
            is_breaking = "!" in subject or "BREAKING" in subject.upper()
            category = self.CATEGORIES.get(cat_key, "🔧 Other")
            return category, scope, is_breaking

        # Fallback: try to infer category from keywords
        subject_lower = subject.lower()
        if any(kw in subject_lower for kw in ["fix", "bug", "patch", "hotfix"]):
            return "🐛 Bug Fixes", "", False
        elif any(kw in subject_lower for kw in ["add", "feature", "new", "implement"]):
            return "✨ Features", "", False
        elif any(kw in subject_lower for kw in ["doc", "readme", "comment"]):
            return "📚 Documentation", "", False
        elif any(kw in subject_lower for kw in ["test", "spec", "coverage"]):
            return "🧪 Tests", "", False
        elif any(kw in subject_lower for kw in ["refactor", "clean", "restructure"]):
            return "♻️ Refactoring", "", False
        elif any(kw in subject_lower for kw in ["perf", "speed", "optimize", "fast"]):
            return "⚡ Performance", "", False

        return "🔧 Other", "", False

    def get_tags(self) -> List[Dict[str, Any]]:
        """Get all git tags with their commit info."""
        output = self._run_git([
            "for-each-ref",
            "--format=%(refname:short)%x00%(objectname:short)%x00%(taggerdate:iso-strict)%x00%(subject)",
            "refs/tags"
        ])

        tags = []
        for line in output.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\x00")
            if len(parts) >= 2:
                try:
                    date = datetime.fromisoformat(parts[2].replace("Z", "+00:00"))
                except (ValueError, IndexError):
                    date = datetime.now()
                tags.append({
                    "name": parts[0],
                    "commit": parts[1],
                    "date": date,
                    "message": parts[3] if len(parts) > 3 else "",
                })
        return tags

    def get_stats(self, commits: List[Commit]) -> Dict[str, Any]:
        """Calculate statistics from commits."""
        if not commits:
            return {}

        authors = {}
        categories = {}
        files = set()
        total_insertions = 0
        total_deletions = 0

        for commit in commits:
            authors[commit.author] = authors.get(commit.author, 0) + 1
            categories[commit.category] = categories.get(commit.category, 0) + 1
            files.update(commit.files_changed)
            total_insertions += commit.insertions
            total_deletions += commit.deletions

        return {
            "total_commits": len(commits),
            "unique_authors": len(authors),
            "top_author": max(authors, key=authors.get) if authors else "",
            "author_commits": authors,
            "categories": categories,
            "unique_files": len(files),
            "total_insertions": total_insertions,
            "total_deletions": total_deletions,
            "date_range": {
                "first": min(c.date for c in commits),
                "last": max(c.date for c in commits),
            },
        }


class GitChronicleError(Exception):
    """Custom exception for GitChronicle errors."""
    pass
