from errors import WrongAssumptionError
from urllib import request


def get_dependency_list(library_name,version=None):
    """
    Takes in library name as a string and optional version number as a string
    Returns list of dependencies and their respective versions
    If no library version is specified, returns dependencies for the latest version of the library
    """
    # need to imitate pip install dry run
    
    return


def get_latest_version_number_from_pypi(library_name):
    '''
    Takes in library name as string, looks it up on pypi, and returns 
    current version number as string
    '''
    url = f"https://pypi.org/project/{library_name}/"
    try:
        result = request.urlopen(url)
        binary_data = result.read()
        data = binary_data.decode('utf-8')
        fulltitle = _hacky_parse_for_library_title(data)
        try: 
            name, version = fulltitle.split(' ')
            return version
        except:
            raise WrongAssumptionError('get_latest_version',f"unable to split name and version properly. Full text is: \n{fulltext}")
            return None
    except:
        raise WrongAssumptionError('get_latest_version',f"unable to connect to {url}")
        return None


def _hacky_parse_for_library_title(html_string):
    classname_start = html_string.find("package-header__name")
    
    inner_start = html_string[classname_start:].find(">")
    text_start = inner_start + classname_start + 1
    
    inner_end = html_string[classname_start:].find("<")
    text_end = inner_end + classname_start
    
    return html_string[text_start:text_end].strip()