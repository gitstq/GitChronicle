"""Tests for narrative module."""

import pytest
from datetime import datetime
from gitchronicle.git_parser import Commit
from gitchronicle.narrative import NarrativeEngine, NarrativeSection


class TestNarrativeEngine:
    """Test NarrativeEngine class."""

    def test_init(self):
        """Test initialization."""
        engine = NarrativeEngine("hero")
        assert engine.style == "hero"

        engine = NarrativeEngine("invalid")
        assert engine.style == "journal"  # fallback

    def test_generate_changelog_empty(self):
        """Test changelog with no commits."""
        engine = NarrativeEngine()
        result = engine.generate_changelog([])
        assert "Changelog" in result

    def test_generate_changelog(self):
        """Test changelog generation."""
        engine = NarrativeEngine()
        commits = [
            Commit(
                hash="a", short_hash="a1", author="Alice", email="a@e.com",
                date=datetime(2024, 1, 1), message="m", subject="feat: add feature",
                category="✨ Features",
            ),
            Commit(
                hash="b", short_hash="b1", author="Bob", email="b@e.com",
                date=datetime(2024, 1, 2), message="m", subject="fix: resolve bug",
                category="🐛 Bug Fixes",
            ),
        ]
        result = engine.generate_changelog(commits, version="v1.0.0")
        assert "v1.0.0" in result
        assert "✨ Features" in result
        assert "🐛 Bug Fixes" in result
        assert "add feature" in result
        assert "resolve bug" in result

    def test_generate_story(self):
        """Test story generation."""
        engine = NarrativeEngine("adventure")
        commits = [
            Commit(
                hash="a", short_hash="a1", author="Alice", email="a@e.com",
                date=datetime(2024, 1, 1), message="m", subject="feat: new castle",
                category="✨ Features",
            ),
        ]
        result = engine.generate_story(commits)
        assert "Adventure" in result
        assert "castle" in result

    def test_generate_release_notes(self):
        """Test release notes generation."""
        engine = NarrativeEngine()
        commits = [
            Commit(
                hash="a", short_hash="a1", author="Alice", email="a@e.com",
                date=datetime(2024, 1, 1), message="m", subject="feat: new feature",
                category="✨ Features", is_breaking=True,
            ),
            Commit(
                hash="b", short_hash="b1", author="Bob", email="b@e.com",
                date=datetime(2024, 1, 2), message="m", subject="fix: bug fix",
                category="🐛 Bug Fixes",
            ),
        ]
        result = engine.generate_release_notes(commits, "v1.0.0")
        assert "v1.0.0" in result
        assert "Breaking Changes" in result
        assert "new feature" in result
        assert "bug fix" in result
        assert "Alice" in result
        assert "Bob" in result

    def test_group_by_category(self):
        """Test commit grouping by category."""
        engine = NarrativeEngine()
        commits = [
            Commit(hash="a", short_hash="a", author="A", email="a@e.com",
                   date=datetime(2024, 1, 1), message="m", subject="feat: x",
                   category="✨ Features"),
            Commit(hash="b", short_hash="b", author="B", email="b@e.com",
                   date=datetime(2024, 1, 2), message="m", subject="fix: y",
                   category="🐛 Bug Fixes"),
            Commit(hash="c", short_hash="c", author="C", email="c@e.com",
                   date=datetime(2024, 1, 3), message="m", subject="feat: z",
                   category="✨ Features"),
        ]
        groups = engine._group_by_category(commits)
        assert len(groups) == 2
        assert groups[0].title == "✨ Features"
        assert len(groups[0].commits) == 2
        assert groups[1].title == "🐛 Bug Fixes"
        assert len(groups[1].commits) == 1
