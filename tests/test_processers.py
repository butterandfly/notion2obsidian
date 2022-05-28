from notion2obsidian.n2o import delete_emptylines, process_notelinks

def test_delete_emptylines():
    content = '''
A

B
'''
    assert delete_emptylines(content) == 'A\nB'

    # Insert an empty line before a heading
    content = '''A
# B
'''
    assert delete_emptylines(content) == 'A\n\n# B'

    content = '''
A

```python
print('Hello!')

```'''

    assert delete_emptylines(content) == '''A
```python
print('Hello!')
```'''

def test_process_notelinks():
    content = '''
[Altair & Vega-Lite](Altair%20&%20Vega-Lite%2048556c3599274926980027a08882551e.md)
[Scikit-Learn](Scikit-Learn%206dd42dbac1a147ceacf7051db282d525.md)
[A: B](A%20B%202b5159a01c2e4638810c09c70c9cb941.md)
'''
    mapping = {
        'Altair & Vega-Lite 48556c3599274926980027a08882551e.md': 'Altair & Vega-Lite',
        'Scikit-Learn 6dd42dbac1a147ceacf7051db282d525.md': 'Scikit-Learn',
        'A B 2b5159a01c2e4638810c09c70c9cb941.md': 'A B'
    }

    assert process_notelinks(content, mapping) == '''
[[Altair & Vega-Lite]]
[[Scikit-Learn]]
[[A B]]
'''
