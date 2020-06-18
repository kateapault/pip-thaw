from urllib import request

def get_latest_version(package_name):
    url = f"https://pypi.org/project/{package_name}/"
    result = request.urlopen(url)
    binary_data = result.read()
    data = binary_data.decode('utf-8')
    
    fulltitle = hacky_parse_for_package_title(data)
    name, version = fulltitle.split(' ')
    return version


def hacky_parse_for_package_title(html_string):
    classname_start = html_string.find("package-header__name")
    
    inner_start = html_string[classname_start:].find(">")
    text_start = inner_start + classname_start + 1
    
    inner_end = html_string[classname_start:].find("<")
    text_end = inner_end + classname_start
    
    return html_string[text_start:text_end].strip()