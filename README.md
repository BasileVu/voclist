# voclist
A simple app to create vocabulary lists and manage them.

## Context
Do you know that feeling when you're learning something new, you need to write it down somewhere to review it later ? 
As I'm learning japanese, that's exactly what I did. I began by simply creating a text file where I put the new words I learned, but
as I added more and more, I wanted to try to group them by categories. The problem is that often, a word can belong to multiple 
categories (will you put "salmon" under the "animal" category or the "food" one ?), and as the file grows, it can become 
difficult to find a word.

I began to develop this app with the idea that, while providing almost the same functionalities as a text file filled with simply 
words and their translations, the words can belong to multiple categories instead of just one.
That, and I wanted to play with flask and sqlalchemy.

## Installation and usage
1. Have python 3 installed and pip ready
2. Download or clone the repo. 
3. Go to the folder (inside "voclist") and type `$ pip install -r requirements.txt`.
4. Run the server by entering `$ python runserver.py`. The default address and port are `127.0.0.1` and `5000`. You can easily change
them by editing the `voclist.cfg` configuration file.

That's it, you can open your browser, go to the address you specified and create your voclists!
