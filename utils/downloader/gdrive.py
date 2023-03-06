from requests import get


def get_response(url: str) -> bytes:
    """ Return the response data in `bytes`. """
    # Get the id
    _id = url.rsplit('/', 2)[-2]

    # Download url prefix
    prefix = 'https://drive.google.com/uc?export=download&id='

    # Get the url response
    r = get(prefix + _id)
    r.raise_for_status()

    return r.content


def download(url: str, filename: str, file_ext: bool = False) -> None:
    """Download and save the data in `downloads/` folder.

    `Note:` Maybe the **file extension** differ from actual extension.
    So, if you find problem try to fix it.

    Args:
        url (str): Google drive files url.
        filename (str): Provide the filename of the file to be saved.
    """
    data = get_response(url)

    if not file_ext:
        ext = ('.docx' if 'docs' in url else
               '.ipynb' if 'drive' in url or 'colab' in url else
               '.pdf')
    else:
        ext = ''

    try:
        with open(f'downloads/{filename + ext}', 'wb') as f:
            f.write(data)
    except FileNotFoundError:
        raise FileNotFoundError('To download please create a directory as `downloads` or \
            run `main.py` to maintain the directory structure.')
