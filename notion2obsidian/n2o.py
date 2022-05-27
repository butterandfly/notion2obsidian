import re
import os
import glob
import shutil
import urllib.parse

log = print

# Regex of links
notelink_regex = r'(?<![!])\[([\w\s\d.\-\&\(\)\:\,]+)\]\(([\w\d.\/?=#%!*\-\(\)\&\,]+\.md)\)'
filelink_regex = r'\[([\w\s\d.\%\,]+)\]\(([\w\d.\/?=#%!*\,]+\.((png)|(pdf)|(csv)))\)'

def process_filelinks(content: str) -> str:
    # Get regex matches
    pattern = re.compile(filelink_regex)
    matches = pattern.finditer(content)

    new_content = content

    for match in matches:
        # Gen new link
        whole_str, file_desc, file_path = match.group(
            0), match.group(1), match.group(2)
        new_image_path = os.path.join('attachments', file_path)
        new_link = f'[{file_desc}]({new_image_path})'

        # Replace new link
        new_content = new_content.replace(whole_str, new_link)
        log(f'{whole_str} -> {new_link}', 'sub')

    return new_content


def process_notelinks(content: str, mapping: dict) -> str:
    # Get regex matches
    note_pattern = re.compile(notelink_regex)
    matches = note_pattern.finditer(content)

    new_content = content

    # Loop through every match
    for match in matches:
        # Get the note name and path
        whole_str, _, note_path = match.group(
            0), match.group(1), match.group(2)
        note_path_withid = note_path.split('/')[-1]
        decoded_name = urllib.parse.unquote(note_path_withid)

        # Replace new link
        new_note_name = mapping[decoded_name].split('.md')[0]
        new_link = f'[[{new_note_name}]]'
        new_content = new_content.replace(whole_str, new_link)
        log(f'{whole_str} -> {new_link}', 'sub')

    return new_content


def delete_emptylines(content: str) -> str:
    in_codeblock = False
    lines = []

    for line in content.split('\n'):
        if line.startswith('```'):
            if in_codeblock:
                in_codeblock = False
            else:
                in_codeblock = True
            lines.append(line)
            continue

        if line == '':
            continue

        # Insert a empty line before headings
        if line.startswith('#') and not in_codeblock:
            lines.append('')

        lines.append(line)

    log('Deleted empty lines', 'sub')
    return '\n'.join(lines)

def process_all_md(dest: str, mapping: dict, args: dict):
    """
    Process all md files in dest.
    """

    log('Start processing all md files', 'info')

    mdfiles = glob.glob(os.path.join(dest, "*.md"))
    for mdfile in mdfiles:
        log(f'Processing {mdfile}', 'info')

        with open(mdfile, 'r') as f:
            content = '\n'.join(f.readlines())

        new_content = process_filelinks(content)
        new_content = process_notelinks(new_content, mapping)

        # Optional settings
        if args['delete_emptylines']:
            new_content = delete_emptylines(new_content)

        with open(mdfile, 'w') as f:
            f.write(new_content)

def copy_all_md(folder: str, dest: str) -> dict:
    """
    Copy all md files in folder to dest, with a new non-id name.

    Return a map of old file name to new file name.
    """
    md_mapping = {}

    log('Start copying all md files', 'info')

    mdfiles = glob.glob(os.path.join(folder, "*.md"))
    for mdfile in mdfiles:
        # Get file name
        file_name = os.path.basename(mdfile)
        base_name = os.path.splitext(file_name)[0]

        # Gen new name
        base_name_noid = ' '.join(base_name.split(' ')[:-1])
        new_file_name = base_name_noid + '.md'

        # Replace inlegal characters
        inlegal_characters = ['\\', '/', ':', '[', ']', '|', '#', '^']
        for c in inlegal_characters:
            new_file_name = new_file_name.replace(c, ' ')

        # Save to mapping
        # If file name is already in mapping, use the original name
        if new_file_name in md_mapping.values():
            new_file_name = file_name

        # Copy file
        new_path = os.path.join(dest, new_file_name)
        shutil.copyfile(mdfile, new_path)
        md_mapping[file_name] = new_file_name

        log(f'Copied: {file_name} -> {new_file_name}', 'sub')

    return md_mapping


def copy_all_attachments(src: str, dest: str) -> None:
    log('Start copying all attachments', 'info')

    file_types = ['png', 'pdf', 'csv']

    paths = glob.glob(os.path.join(src, "*"))
    for path in paths:
        filename = path.split('/')[-1]
        ext = filename.split('.')[-1]
        if ext in file_types:
            new_path = os.path.join(dest, 'attachments', filename)
            shutil.copyfile(path, new_path)
            log(f'{path} -> {new_path}', 'sub')


def notion2obsidian_nosubdir(args: dict):
    folder = args['src']
    dest = args['output']

    input_check(folder)

    if dest == '':
        dest = folder + '_obsidian'
    dest_check(dest)

    log('Start convert...', 'info')

    create_obsidian_folders(dest)

    # Copy all attachments
    copy_all_attachments(folder, dest)

    # Copy all md
    mapping = copy_all_md(folder, dest)
    process_all_md(dest, mapping, args)

    log('🎉 Converting finished!', 'success')


def create_obsidian_folders(dest: str):
    """
    Create the dest folder and subfolders.
    """
    os.makedirs(dest)
    attachments_folder = os.path.join(dest, 'attachments')
    os.makedirs(attachments_folder)


def input_check(folder: str):
    if not os.path.exists(folder):
        log(f'{folder} not exists!', 'error')
        raise


def dest_check(dest: str):
    if os.path.exists(dest):
        log(f'{dest} already exists!', 'error')
        raise
