__package__ = "tests.unit"

from ipfskvs.index import Index

import pytest


@pytest.fixture
def index_fixture() -> Index:
    """Create sample data."""
    return Index(index={
        'key1': '00000000-0000-0000-0000-000000000001',
        'key2': '00000000-0000-0000-0000-000000000002',
        'key3': '00000000-0000-0000-0000-000000000003'
    })


def test_matches_returns_true_when_indexes_are_equal(index_fixture: Index) -> None:  # noqa: E501
    """Test with identical indexes."""
    other_index = Index(index={
        'key1': '00000000-0000-0000-0000-000000000001',
        'key2': '00000000-0000-0000-0000-000000000002',
        'key3': '00000000-0000-0000-0000-000000000003'
    })

    assert index_fixture.matches(other_index)


def test_matches_returns_false_when_indexes_are_not_equal(index_fixture: Index) -> None:  # noqa: E501
    """Test with an incompatible index due to mismatch."""
    other_index = Index(index={
        'key1': '00000000-0000-0000-0000-000000000001',
        'key2': '00000000-0000-0000-0000-000000000005',
        'key4': '00000000-0000-0000-0000-000000000004',
    })

    assert not index_fixture.matches(other_index)


def test_matches_returns_false_when_other_index_has_missing_key(index_fixture: Index) -> None:  # noqa: E501
    """Test with an incompatible index due to a missing key."""
    other_index = Index(index={
        'key1': '00000000-0000-0000-0000-000000000001',
        'key2': '00000000-0000-0000-0000-000000000002'
    })

    assert not index_fixture.matches(other_index)
