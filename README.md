# Notion2obsidian
Notion2obsidian is a utility and python package for convert Notion exported markdown files to Obsidian markdown files.

## Important
For now `notion2obsidian` only supports the "no sub folder" structure. Make sure you use the exported options like this:

![No sub folder](https://raw.githubusercontent.com/butterandfly/notion2obsidian/main/images/no%20sub%20folder.png)

## Installation
```bash
pip install notion2obsidian
```

## Usage
```bash
notion2obsidian notion_folder -o dest -l
```

Since Notion will make tons of empty lines into the exported files, you can use `-l` to delete empty lines (but keep one before a heading line).

## How it works
### Markdown files
`notion2obsidian` won't change the folder structure, but the markdown file's name. Since every md file that Notion exported has an id in the name, `notion2obsidian` will remove the id, unless there are two md files use the smae name.
Note that some characters, aka `#^[]|\/:`, are inleagle for the markdown file name in Obsidian, so they will be remove in the name.

### Attachments
Attachment files, like `.png`, `.pdf` and `csv`, will be all moved to the `attachments` folder without changing the name.

### Links in markdown files
There two types of link will be change:
- Markdown files with relative path
- Attachment files with relative path
Example:
```
[Room 1](Room%201%207a6f70896bfc4e5e976d588412b74370.md) -> [[Room 1]]
[dummy.pdf](dummy.pdf) -> [dummy.pdf](attachments/dummy.pdf)
[Untitled](Untitled%201.png) -> [Untitled](attachments/Untitled%201.png)
```
