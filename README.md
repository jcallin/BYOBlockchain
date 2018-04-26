# BYOBlockchain
A Proof-of-Work distributed ledger experiment. Project modeled off of https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
but with 

* Separated code files for server and proof-of-work
* Added protection against rewritten tx history by implementing hash of previous block into validation computation

Using Python 3.6+
Build a virtual environment to work in
* `virtualenv -p python3 py3_env`
* `py3_env/bin/pip3 install -r requirements.txt`

To test, run 2 nodes locally using `python server.py 5000` `python server.py 5001`

Use [this Postman collection](https://www.getpostman.com/collections/08f4b1a53dc757bb1c6a) to register the nodes with each other, send transactions, mine blocks, and more

