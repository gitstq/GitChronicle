"""Tests for git_parser module."""

import pytest
from datetime import datetime
from gitchronicle.git_parser import Commit, GitParser, GitChronicleError


class TestCommit:
    """Test Commit dataclass."""

    def test_commit_creation(self):
        """Test creating a Commit object."""
        commit = Commit(
            hash="abc123def456",
            short_hash="abc123d",
            author="Test User",
            email="test@example.com",
            date=datetime(2024, 1, 1, 12, 0, 0),
            message="feat: add new feature",
            subject="feat: add new feature",
            category="✨ Features",
        )
        assert commit.hash == "abc123def456"
        assert commit.author == "Test User"
        assert commit.category == "✨ Features"
        assert not commit.is_breaking


class TestGitParser:
    """Test GitParser class."""

    def test_init(self):
        """Test GitParser initialization."""
        parser = GitParser(".")
        assert parser.repo_path == "."

    def test_categorize_commit_conventional(self):
        """Test categorizing conventional commits."""
        parser = GitParser(".")

        cat, scope, breaking = parser._categorize_commit("feat: add login")
        assert cat == "✨ Features"
        assert not breaking

        cat, scope, breaking = parser._categorize_commit("fix(auth): resolve bug")
        assert cat == "🐛 Bug Fixes"
        assert scope == "auth"

        cat, scope, breaking = parser._categorize_commit("feat!: breaking change")
        assert cat == "✨ Features"
        assert breaking

    def test_categorize_commit_fallback(self):
        """Test fallback categorization."""
        parser = GitParser(".")

        cat, _, _ = parser._categorize_commit("Fixed a bug in login")
        assert cat == "🐛 Bug Fixes"

        cat, _, _ = parser._categorize_commit("Added new dashboard feature")
        assert cat == "✨ Features"

        cat, _, _ = parser._categorize_commit("Updated documentation")
        assert cat == "📚 Documentation"

    def test_get_stats_empty(self):
        """Test stats with empty commits."""
        parser = GitParser(".")
        stats = parser.get_stats([])
        assert stats == {}

    def test_get_stats(self):
        """Test stats calculation."""
        parser = GitParser(".")
        commits = [
            Commit(
                hash="a", short_hash="a", author="Alice", email="a@e.com",
                date=datetime(2024, 1, 1), message="m", subject="feat: x",
                category="✨ Features",
            ),
            Commit(
                hash="b", short_hash="b", author="Bob", email="b@e.com",
                date=datetime(2024, 1, 2), message="m", subject="fix: y",
                category="🐛 Bug Fixes",
            ),
            Commit(
                hash="c", short_hash="c", author="Alice", email="a@e.com",
                date=datetime(2024, 1, 3), message="m", subject="feat: z",
                category="✨ Features",
            ),
        ]
        stats = parser.get_stats(commits)
        assert stats["total_commits"] == 3
        assert stats["unique_authors"] == 2
        assert stats["top_author"] == "Alice"
        assert stats["categories"]["✨ Features"] == 2
        assert stats["categories"]["🐛 Bug Fixes"] == 1
