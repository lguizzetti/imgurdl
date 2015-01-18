import re

def parse_id(path):
    """ Takes in either a URL or Imgur album or picture name (path), and
    returns just the string ID of the image(s).
    """
    domain_pattern = r"^(https://|http://)?(www.)?(imgur.com)?(/a/)?"
    id_pattern = r"([a-zA-Z0-9]{1,})(/)?$"

    # If the path matches a URL pattern, then drop the URL domain portion.
    stripped_path = re.sub(domain_pattern, '', path, flags = re.IGNORECASE)

    # Match the string ID of the Imgur album or image
    id = re.search(id_pattern, stripped_path).groups()[0]
    return id


def is_album(path):
    """ Tries to determine if the supplied path is for an imgur album.

    Returns True if an album flag is found. False if unknown or not detected.
    """
    album_pattern = r"(/a/){1}"
    result = re.search(album_pattern, path, flags = re.IGNORECASE)
    if result is not None:
        return True
    
    return False



if __name__ == '__main__':

    test_albums = [ "https://imgur.com/a/Dhjed", "https://imgur.com/a/Dhjed/",
            	"http://imgur.com/a/Dhjed", "http://imgur.com/a/Dhjed/",
            	"https://www.imgur.com/a/Dhjed", "https://www.imgur.com/a/Dhjed/",
                "http://www.imgur.com/a/Dhjed", "http://www.imgur.com/a/Dhjed/",
            	"imgur.com/a/Dhjed", "imgur.com/a/Dhjed/",
            	"imgur.com/a/Dhjed", "imgur.com/a/Dhjed/",
            	"www.imgur.com/a/Dhjed", "www.imgur.com/a/Dhjed/",
            	"www.imgur.com/a/Dhjed", "www.imgur.com/a/Dhjed/",
            	"Dhjed" ]

    
    test_images = [ "https://imgur.com/r4KjYry", "https://imgur.com/r4KjYry/",
                "https://www.imgur.com/r4KjYry", "https://www.imgur.com/r4KjYry/",
                "http://imgur.com/r4KjYry", "http://imgur.com/r4KjYry/",
                "http://www.imgur.com/r4KjYry", "http://www.imgur.com/r4KjYry/",
                "imgur.com/r4KjYry", "imgur.com/r4KjYry/",
                "www.imgur.com/r4KjYry", "www.imgur.com/r4KjYry/",
                "imgur.com/r4KjYry", "imgur.com/r4KjYry/",
                "www.imgur.com/r4KjYry", "www.imgur.com/r4KjYry/",
                "r4KjYry" ]
    