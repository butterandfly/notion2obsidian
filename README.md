## Folder Structure
`notion2obsidian` won't change the folder structure, but the markdown file's name. Since every md file that Notion exported has an id in the name, `notion2obsidian` will remove the id, unless there are two md files use the smae name.
Note that some characters, aka `#^[]|\/:`, are inleagle for the markdown file name in Obsidian, so they will be remove in the name.

Attachment files, like `.png`, `.pdf` and so on, will be all moved to the `attachments` folder without changing the name.

Here is the exmaple:
```bash

```

## Links in `.md`
Two kinds of links will be updated:
- Local markdown file links, like
- Local attachments links, like


