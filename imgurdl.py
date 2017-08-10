import re
import sys
import getopt
import os
import urllib3
import io
from bs4 import BeautifulSoup as bs

class ImgurDL:
    """ A class to download images and albums from Imgur (TM).

    This script can be called from the command-line or the class can be used 
    on its own.
    """

    def __init__(self):
        # Flag to use the default directory, which will be the same as the 
        # album or image ID. (E.g., /a/abcde will be saved to ./abcde/)
        self.use_default_directory = True

        # Output directory. If specified, all downloads go into this directory.
        self.output_dir = os.path.dirname(os.path.realpath(__file__))

        # Set of 2-tuples containing the string tokens of each image and album
        self.token_list = set()     # each item is (token, token type}
                                    # where type is either "image" or "string"

        # List of 3-tuples containing the URLs to fetch and the output directory.
        self.download_list = set()  # each item is (url, output dir, output file)

        # Establish a HTTP connection pool manager
        self.http = urllib3.PoolManager()

    def parse_token(self, token):
        """ Takes in either a URL or Imgur album or picture name (token), and
        returns just the string token of the image(s).
        """
        domain_pattern = r"(https://|http://)?(www.)?(imgur.com)?(/a/)?"
        token_pattern = r"([a-zA-Z0-9]{1,})(/)?$"

        # If the token matches a URL pattern, then drop the URL domain portion.
        stripped_id = re.sub(domain_pattern, '', token, flags = re.IGNORECASE)

        # Match the string ID of the Imgur album or image
        token = re.search(token_pattern, stripped_id).groups()[0]
        return token

    def is_album(self, url):
        """ Parses a URL for the album directory. 

        Return True if the album URL is found (e.g., /a/token, or imgur.com/a/token)
        Return False otherwise.
        """
        domain_pattern = r"(imgur.com/)?(a/)"
        result = re.search(domain_pattern, url, flags = re.IGNORECASE)
        if result is None:
            return False
        else:
            return True

    def extract_urls(self, token_list):
        """ From the converted token list, the image files are scraped from Imgur and
        stored in a list for download.
        """
        # iterate over all collected tokens
        for item in token_list:
            (token, token_type) = item

            # Get the temporary NoScript URL. This will extract the URL from the HTML page.
            if token_type == "album":
                req_url = "http://i.imgur.com/a/{0}/noscript".format(token)
            elif token_type == "image":
                req_url = "http://i.imgur.com/{0}".format(token)
            else:
                print("Something went wrong!")

            # All of the image links are inside div tags in the body
            html = self.http.urlopen("GET", req_url, preload_content = False)

            # create BeautifulSoup object for html parsing
            soup = bs(html.data, "html.parser")

            # set up list for links
            filenames = []

            # find all post image links
            data = soup.findAll("div", attrs={"class":"post-image"})
            for div in data:
                for a in div:
                    if a.name == "a":
                        # links are in the form //i.imgur.com/[token].[file extension]
                        # this will take only the filename
                        filenames.append(a["href"].split('/')[-1])

            # Extract each matched URL and add it to a set.
            domain = "http://i.imgur.com/"
            for im_filename in filenames:
                # Make sure that images from an album go in their own folder.
                if token_type == "album":
                    url = "{0}download/{1}".format(domain, im_filename)
                    download_dir = os.path.join(self.output_dir, token)
                    download_path = "{0}/{1}".format( download_dir, im_filename )

                # individual images go straight to the output directory
                elif token_type == "image":
                    url = "{0}download/{1}".format(domain, im_filename)
                    download_dir = self.output_dir
                    download_path = "{0}/{1}".format( download_dir, im_filename )
                self.download_list.add( (url, download_dir, im_filename) )


    def save_images(self):
        """ Save the images to the disk. """        
        for url, odir, ofile in sorted(list(self.download_list)):
            
            # Produce the absolute output path.
            opath = os.path.abspath(os.path.join(odir, ofile))

            # Make any new directories as needed.
            if not os.path.isdir(odir):
                os.makedirs(odir)

            # Actually download the file finally.
            with open(opath, 'wb+') as f:
                req = self.http.urlopen("GET", url, preload_content=False)
                buf = io.BufferedReader(req)
                f.write(buf.read())
                f.close()

        # Clean up by closing all connections.
        self.http.clear()


    @staticmethod
    def usage():
        """ Prints a help message. """
        msg = ['Description: Quickly and easily download imgur images and albums.',
        'High qualiity images are saved in sub-directories for albums, or output',
        'path for images.\n',
        'Usage:\n',
        '$ python imgurdl.py [-d] [-a "albums ..."] [-i "images ..."] [-o output-dir]',
        '(Both albums and images are identified by URLs or string tokens.)',
        '\n$ python imgurdl.py [-o output-dir] [/a/album1 /a/album2...] [images...]\n',
        'Options:\n',
        '-a="...", --albums="URLs or tokens"\tAlbums to download.',
        '                                        A token looks like "ad213ea".\n',
        '-i="...", --images="image URLs or tokens"     Images to download.\n',
        '-o="...", --out="/out/dir"     Output path. Default is the script path.\n',
        '-d, --debug\n',
        '-h, --help\n',
        'Notes:',
        '\nURLs and tokens can be mixed. For example, downloading multiple images and albums:',
        '$ python imgurdl.py -a="H7phc http://imgur.com/a/CYDeW" -i="zMZSWtg i.imgur.com/3PmuS9F"\n',
        'Alternatively, by prefixing albums with "/a/", followed by any image URLs:',
        '$ python imgurdl.py [--out=path] [/a/albums ...] [images ...]']
        print("\n".join(msg))


def debug(imgur):
    """ Print debug information when calling this script from the command line. """
    if _debug:
        print("Debug mode: On")
        print("\nOutput directory: {0}".format(imgur.output_dir))
        print("====== Downloads ========")
        
        i = 0
        for item in imgur.token_list:
            i += 1
            (token, token_type) = item
            print("{0}. {1}: {2}".format(i, token_type.title(), token))
        print("\n")
        

def main(argv):
    global _debug
    _debug = False
    _album_flag = False
    _img_flag = False

    #Set the command-line flags that will be used by the script.
    try:
        opts, args = getopt.getopt(argv, "ha:i:o:d", ["help", "albums=", "images=", "out=", "debug"])
    except getopt.GetoptError:
        # Exit if there is an unrecognized flag passed, printing the usage guide.
        ImgurDL.usage()
        sys.exit()

    # Instantiate an imgur downloader.
    imgur = ImgurDL()

    # Process the command line flags.
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            ImgurDL.usage()
            sys.exit()
        
        elif opt in ("-d", "--debug"):
            # Enable extra debug information to be printed to stdout.
            _debug = True

        elif opt in ("-o", "--out"):
            imgur.use_default_directory = False
            imgur.output_dir = arg
        
        elif opt in ("-a", "--albums"):
            album_args = arg.split(" ")
            _album_flag = True

            for album in album_args:
                token = imgur.parse_token(album)
                imgur.token_list.add( (token, "album") )
            
        elif opt in ("-i", "--images"):
            image_args = arg.split(" ")
            _img_flag = True
            for image in image_args:
                token = imgur.parse_token(image)
                imgur.token_list.add( (token, "image") )

    # Look at the command-line arguments now.
    # Exit the program if no useful download tokens were passed.
    if len(args) > 0:
        album_args = []
        img_args = []
        for a in args:
            a_token = imgur.parse_token(a)
            if imgur.is_album(a):
                album_args.append(a_token)
            else:
                img_args.append(a_token)

        for token in album_args:
            imgur.token_list.add( (token, "album") )
        else:
            _album_flag = True
        
        for token in img_args:
            imgur.token_list.add( (token, "image") )
        else:
            _img_flag = True
    
    # Download the images passed in the options.
    if _album_flag or _img_flag:
        # If requested, print debug information.
        debug(imgur)
    
        imgur.extract_urls(imgur.token_list)
        imgur.save_images()
    else:
        ImgurDL.usage()

if __name__ == '__main__':
    main(sys.argv[1:])
