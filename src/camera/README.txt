Just some notes about the process_img requirements


It relies on zbar to do the qr processing. There is a python wrapper on
top of zbar called zbarlight.

It also uses Pillow, which contains the old seaworthy PIL code.

I had to do the following to get these packages up and running on my mac:

brew install zbar
pip install zbarlight
pip install Pillow

Now, if we were being really good python programmers, we would be using
virtualenv to do the pip installing - but I haven't set that up.