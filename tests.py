from typing import Tuple, List
import pytest
from utils import identify_changes


list1 = [(1, True), (2, True), (3, False)]

list2 = [(1, True), (2, True), (3, False), (4, True)]
def test_output2():
    expected_matched = [(1, True), (2, True), (3, False)]
    expected_changed = []
    expected_added = [(4, True)]
    expected_deleted = []
    assert identify_changes(list1, list2) == (expected_matched, expected_changed, expected_added, expected_deleted)

list3 = [(1, True), (2, True), (3, True), (4, True)]
def test_output3():
    expected_matched = [(1, True), (2, True)]
    expected_changed = [((3, False), (3, True))]
    expected_added = [(4, True)]
    expected_deleted = []
    assert identify_changes(list1, list3) == (expected_matched, expected_changed, expected_added, expected_deleted)

list4 = [(1, True), (5, True), (2, True), (6, False), (3, False)]
def test_output4():
    expected_matched = [(1, True), (2, True), (3, False)]
    expected_changed = []
    expected_added = [(5, True), (6, False)]
    expected_deleted = []
    assert identify_changes(list1, list4) == (expected_matched, expected_changed, expected_added, expected_deleted)

list5 = [(1, True), (5, True), (2, True), (6, False)]
def test_output5():
    expected_matched = [(1, True), (2, True)]
    expected_changed = []
    expected_added = [(5, True), (6, False)]
    expected_deleted = [(3, False)]
    assert identify_changes(list1, list5) == (expected_matched, expected_changed, expected_added, expected_deleted)

list6 = [(1, True), (5, True), (6, False), (3, False)]
def test_output6():
    expected_matched = [(1, True), (3, False)]
    expected_changed = []
    expected_added = [(5, True), (6, False)]
    expected_deleted = [(2, True)]
    assert identify_changes(list1, list6) == (expected_matched, expected_changed, expected_added, expected_deleted)

list7 = [(1, False), (2, True), (3, True), (5, True), (6, False)]
def test_output7():
    expected_matched = [(2, True)]
    expected_changed = [((1, True), (1, False)), ((3, False), (3, True))]
    expected_added = [(5, True), (6, False)]
    expected_deleted = []
    assert identify_changes(list1, list7) == (expected_matched, expected_changed, expected_added, expected_deleted)

list8 = [(2, True), (3, True), (5, True), (6, False), (1, False)]
def test_output8():
    expected_matched = [(2, True)]
    expected_changed = [((1, True), (1, False)), ((3, False), (3, True))]
    expected_added = [(5, True), (6, False)]
    expected_deleted = []
    assert identify_changes(list1, list8) == (expected_matched, expected_changed, expected_added, expected_deleted)
