# imgur Downloader

This Python script downloads images and entire albums from imgur. It contains a command-line interface and has a python class that can be used on its own. Images are saved at high resolution.

## Requirements

Python >= 3.3

## Command-Line Usage

    $ python imgurdl.py [-d] [-a "album urls or tokens"] [-i "image urls or tokens"] [-o output-dir] ...
    
*Note that the script is not sensitive to the positional order of arguments.*

To download a single album to the path */home/leo/downloads/* using the album token: 

    $ python imgurdl.py -a CYDeW -o "/home/leo/downloads/"

or using the full album URL:

    $ python imgurdl.py -a http://imgur.com/a/CYDeW -o "/home/leo/downloads/"

To download a single image to the same path as the script by using the image token: 

    $ python imgurdl.py -i 3PmuS9F

or using the full image URL:

    $ python imgurdl.py -i="http://i.imgur.com/3PmuS9F"

To download multipe albums, you can also mix URLs and tokens togeter:

    $ python imgurdl.py -a="H7phc http://imgur.com/a/CYDeW"

To download multiple images (and again you can mix URLs and tokens):

    $ python imgurdl.py -i="zMZSWtg https://i.imgur.com/Natfc91 http://i.imgur.com/3PmuS9F"

You can also download images and albums in the same command:

    $ python imgurdl.py -a="..." -i="..."

An alternative use is to specify albums by an album prefix ('/a/'), followed by any image URLs or tokens. These will be saved to the same path as the script. To specify a different download directory, then the output path must be specified *before* the images and albums.

    $ python imgurdl.py [--out=path] [/a/album1 /a/album2 http://url/to/album3] [image URLs or tokens]

## Options

**-a=** *"album URLs or tokens"*, **--albums=** *"album URLs or tokens"*

 * Saves albums into their own sub-foler named by the album string token. Accepts any valid URL, or just the string token (.e., "abCdE123"). Album tokens can also be written with a '/a/' prefix (e.g., /a/abCdE123).

**-i=** *"image URLs or tokens"*, **--images=** *"image URLs or tokens"*

 * Saves images to the download folder. Accepts any valid URL, or just the string token (.e., "abCdE123").

**-o=** */out/dir*, **--out=** */out/dir*

 * Save images and albums into the specified directory. Images are saved in this directory, and albums are stored in a sub-folder under this directory labelled by the album string token. If no output directory is specified, the same path of the script is used by default.

**-d**, **--debug**

 * Prints some additional debug information while running the script.

**-h**, **--help**

 * Prints a description of how to use this script from the command-line.
    
## License

*CC-BY-SA*

## Credits

Written by [Leonardo Guizzetti](https://github.com/leonardicus)

Idea inspired by [imgur album downloader](https://github.com/alexgisby/imgur-album-downloader)
