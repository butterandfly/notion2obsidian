from notion2obsidian.n2o import notelink_regex, filelink_regex
import re

def test_notelink_regex():
    # Test matching a note link 
    # 1. normal note link
    # 2. note link with special characters
  
    content = '[A Note](notepath/A%20Note%20someid.md)'
    result = re.search(notelink_regex, content)
    assert result.group(0) == '[A Note](notepath/A%20Note%20someid.md)'
    assert result.group(1) == 'A Note'
    assert result.group(2) == 'notepath/A%20Note%20someid.md'

    content = '''
  Some words before a link. [A Note](notepath/A%20Note%20someid.md).
  '''
    result = re.search(notelink_regex, content)
    assert result.group(0) == '[A Note](notepath/A%20Note%20someid.md)'

    # Image links
    content = '![Untitled](notepath/Untitled.png)'
    result = re.search(notelink_regex, content)
    assert result == None

    # PDF links
    content = '[paper](notepath/paper.pdf)'
    result = re.search(notelink_regex, content)
    assert result == None

    # Including brackets
    content = '''
  [A (B)](A%20(B)%2088a51152e50148978f58eaf256bddb6f.md)
  '''
    result = re.search(notelink_regex, content)
    assert result.group(
        0) == '[A (B)](A%20(B)%2088a51152e50148978f58eaf256bddb6f.md)'

    # Including `-`
    content = '''
  [A-B](A-B%2088a51152e50148978f58eaf256bddb6f.md)
  '''
    result = re.search(notelink_regex, content)
    assert result.group(
        0) == '[A-B](A-B%2088a51152e50148978f58eaf256bddb6f.md)'

    # Including '&'
    content = '''
  [A&B](A&B%2088a51152e50148978f58eaf256bddb6f.md)
  '''
    result = re.search(notelink_regex, content)
    assert result.group(
        0) == '[A&B](A&B%2088a51152e50148978f58eaf256bddb6f.md)'

    # Including ','
    content = '''
  [a,b](a,b%203610ec047b9a4b06a6347f7926598964.md)
'''
    result = re.search(notelink_regex, content)
    assert result.group(
        0) == '[a,b](a,b%203610ec047b9a4b06a6347f7926598964.md)'

def test_filelink_regex():
    content = '![Untitled%201.png](Untitled%201.png)'
    result = re.search(filelink_regex, content)
    assert result.group(0) == '[Untitled%201.png](Untitled%201.png)'
    assert result.group(2) == 'Untitled%201.png'

    content = '[A Note](notepath/A%20Note%20someid.md)'
    result = re.search(filelink_regex, content)
    assert result == None

    content = '[paper](imagepath/paper.pdf)'
    result = re.search(filelink_regex, content)
    assert result.group(0) == '[paper](imagepath/paper.pdf)'
