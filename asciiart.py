#! /usr/bin/env python3

"""Convert picture to asciiArt, requrie python3.6 or higher.
Dependence:
- fire
- PIL
- numpy
Usage:
- chmod +x asciiart.py
- asciiart.py ${path_to_image} [Height] [Width]
Also, you can remove the filetype ".py" and put it to $HOME/bin/ then enjoy it:)
One example:

                  *&&&&&&&&&&&&&&&&&&&&&+
                 &&&$    &&&&&&&&&&&&&&&&&%
                 &&&&&%&&&&&&&&&&&&&&&&&&&$
                 %%%%%%%%%%%%%&&&&&&&&$$$$$
       +&&&&&&&&&&&&&&&&&&&&&&&$&&&$$$$$$$$ ****** ***
     &&&&&&&&&&&&&&&&&&&&&&&&&&&&$$$$$$$$$$*************
    &&&&&&&&&&&&&&&&&&&&&&&&&&&$$$$$$$$$&$%*************
   *&&&&&&&&&&&&&&&&&&&&&&&&&&$$$$$$$$$# ****************
   +&&&&&&&&&&&&&$%**************************************
    &&&&&&&&&&&&** **************************************
    *&&&&&&&&&&$ ***************************************
      +&&&&&&&&$ *************************************
                 **************************
                 **************************
                 ******************    ****
                   +********************+

"""

import fire
from PIL import Image
import numpy as np
import sys


class AsciiArt:

    DEFAULT_HEIGHT = 20
    DEFAULT_WIDTH = 60
    SYMBOL = list("@#$&%+* ")

    def draw(self, image_path, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH):
        try:
            image = Image.open(image_path).resize((width, height))
            array = np.array(image.convert("L"))
            image.close()
        except FileNotFoundError:
            print(f"{image_path} not exist")
            sys.exit(1)

        array = np.floor((array / 256) * 8)
        result = []
        for i, line in enumerate(array):
            try:
                result.append("".join(map(lambda x: self.SYMBOL[int(x)], line)) + "\n")
            except IndexError:
                print(i)
                sys.exit(1)

        return "".join(result)


if __name__ == "__main__":
    fire.Fire(AsciiArt)
