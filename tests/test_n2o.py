from os import path
import os
import shutil
from notion2obsidian import n2o
import pytest

HERE = path.dirname(path.abspath(__file__))

test_notes = path.join(HERE, 'test_notes')
test_notes_obsidian = path.join(HERE, 'test_notes_obsidian')

real_exported = path.join(HERE, 'House_Notes')
real_exported_obsidian = path.join(HERE, 'House_Notes_obsidian')

def test_create_obsidian_folders():
    dest = test_notes_obsidian
    n2o.create_obsidian_folders(dest)

    assert path.isdir(dest)
    assert path.isdir(path.join(dest, 'attachments'))

def test_copy_all_md():
    src = test_notes
    dest = test_notes_obsidian
    os.makedirs(dest)
    mapping = n2o.copy_all_md(src, dest)

    assert path.isfile(path.join(dest, 'house.md'))

def test_copy_attachments():
    src = test_notes
    dest = test_notes_obsidian
    n2o.create_obsidian_folders(dest)
    n2o.copy_all_attachments(src, dest)

    assert path.isfile(path.join(dest, 'attachments/image 1.png'))
    assert path.isfile(path.join(dest, 'attachments/pdf 1.pdf'))

def test_notion2obsidian_nosubdir():
    src = real_exported
    dest = real_exported_obsidian
    n2o.notion2obsidian_nosubdir({
        'src': src,
        'output': dest,
        'delete_emptylines': True,
    })

    assert path.isdir(dest)
    assert path.isdir(path.join(dest, 'attachments'))
    assert path.isfile(path.join(dest, 'House.md'))
    assert path.isfile(path.join(dest, 'Room 1.md'))
    assert path.isfile(path.join(dest, 'Room 2.md'))
    assert path.isfile(path.join(dest, 'attachments', 'Untitled.png'))
    assert path.isfile(path.join(dest, 'attachments', 'dummy.pdf'))

@pytest.fixture(autouse=True)
def remove_created():
    """Remove created files after each test."""

    yield 

    if path.isdir(test_notes_obsidian):
        shutil.rmtree(test_notes_obsidian)

    if path.isdir(real_exported_obsidian):
        shutil.rmtree(real_exported_obsidian)
