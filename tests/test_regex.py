from notion2obsidian.n2o import notelink_regex, filelink_regex
import re

def test_notelink_regex():
  content = '[This is a note](notepath/some.md)'
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[This is a note](notepath/some.md)'

  content = '''
  Some words. [This is a note](notepath/some.md).
  '''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[This is a note](notepath/some.md)'

  content = '![This is not a note](notepath/some.md)'
  result = re.search(notelink_regex, content)
  assert result == None

  content = '[This is not a md](notepath/some.pdf)'
  result = re.search(notelink_regex, content)
  assert result == None

  # Including space
  content = '''
[A B](A%20B%20e0346a4acffa4151893a6a6cf0e8a5b2.md)
'''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[A B](A%20B%20e0346a4acffa4151893a6a6cf0e8a5b2.md)'

  # Including brackets
  content = '''
  [A (B)](A%20(B)%2088a51152e50148978f58eaf256bddb6f.md)
  '''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[A (B)](A%20(B)%2088a51152e50148978f58eaf256bddb6f.md)'

  # Including dash
  content = '''
  [A-B](A-B%2088a51152e50148978f58eaf256bddb6f.md)
  '''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[A-B](A-B%2088a51152e50148978f58eaf256bddb6f.md)'

  # Including '&'
  content = '''
  [A&B](A&B%2088a51152e50148978f58eaf256bddb6f.md)
  '''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[A&B](A&B%2088a51152e50148978f58eaf256bddb6f.md)'

  # Including ','
  content = '''
  [a,b](a,b%203610ec047b9a4b06a6347f7926598964.md)
'''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[a,b](a,b%203610ec047b9a4b06a6347f7926598964.md)'

  content = '''
 [etc](etc%206b01f2f2e1544d64a16c5dcf32975af0.md) 
  '''
  result = re.search(notelink_regex, content)
  assert result.group(0) == '[etc](etc%206b01f2f2e1544d64a16c5dcf32975af0.md)'
  assert result.group(1) == 'etc'
  assert result.group(2) == 'etc%206b01f2f2e1544d64a16c5dcf32975af0.md'

# def test_imagelink_regex():
#   imagelink_regex = main.imagelink_regex

#   content = '![This is an image](imagepath/some.png)'
#   result = re.search(imagelink_regex, content)
#   assert result.group(0) == '![This is an image](imagepath/some.png)'

#   content = '![Untitled%201.png](Untitled%201.png)'
#   result = re.search(imagelink_regex, content)
#   assert result.group(0) == '![Untitled%201.png](Untitled%201.png)'

def test_filelink_regex():
  content = '![This is an image](imagepath/some.png)'
  result = re.search(filelink_regex, content)
  assert result.group(0) == '[This is an image](imagepath/some.png)'

  content = '![Untitled%201.png](Untitled%201.png)'
  result = re.search(filelink_regex, content)
  assert result.group(0) == '[Untitled%201.png](Untitled%201.png)'
  assert result.group(2) == 'Untitled%201.png'

  content = '[This is a md](imagepath/some.md)'
  result = re.search(filelink_regex, content)
  assert result == None

  content = '[This is a pdf](imagepath/some.pdf)'
  result = re.search(filelink_regex, content)
  assert result.group(0) == '[This is a pdf](imagepath/some.pdf)'