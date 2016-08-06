def sanitize_text(text):
    output = ''
    for line in text.split('\n'):
        output += '{}\n'.format(line.strip())
    return output
