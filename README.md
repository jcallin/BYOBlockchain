# BYOBlockchain
A Proof-of-Work distributed ledger experiment.

## Before cloning the repo,
* `brew install python3`
* `pip3 install virtualenv`

## After cloning the repo, go into the repo folder and run...
Build a virtual environment to work in
* `virtualenv -p python3 py3_env`
* `py3_env/bin/pip3 install -r requirements.txt`
Activate the virtual environment
* `source py3_env/bin/activate`

A virtual environment, when activated, makes sure you are using a version of python installed in py3_env/ instead of your system python. Also, anything you install with `pip install <package>` while the virtualenv is activated will be installed inside py3_env/ instead of installed system wide. This is helpful because you don't want to mess with your system python/python packages.
After running `source py3_env/bin/activate` above, run `which python3`. You should see the output leading to py3_env/bin/python3
  
Deactivate the virtual environment by running
* `deactivate`

Now run `which python3` again, you should see a path that looks like `/usr/local/bin/python3`

Don't worry about the URL below, we'll use it later

Use [this Postman collection](https://www.getpostman.com/collections/08f4b1a53dc757bb1c6a) to register the nodes with each other, send transactions, mine blocks, and more
