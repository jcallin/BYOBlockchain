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

## Testing the blockchain
* Open up 2 terminal windows
* In each window, change directories to the repo folder
* In one, run `python server.py 5000`
* In the other, run `python server.py 5001`
* You now are running 2 blockchain nodes and are ready to send requests to them using Postman

Use [this Postman collection](https://www.getpostman.com/collections/08f4b1a53dc757bb1c6a) to register the nodes with each other, send transactions, mine blocks, and more. You can copy that link and press "import" in Postman to import the collection. Paste the link into the import sections. I've already built the requests for you.
Select each request, and inspect and modify it using the 'body' tab. Send it using the 'send' button

### Follow these steps to test the chain
* Register the nodes with each other using the 2 'register' requests. This lets the nodes talk to each other when updating their chains.
* Submit a transaction to Node 0 using the corresponding request. You can modify the body to specify a sender, a reciever, and an amount
* Include the transaction in a block by asking Node 0 to mine a block using the appropriate request
* Now that Node 0 has a block, ask Node 0 for its chain and inspect it. Our transaction has been included in this block along with the miner's reward transaction to himself.
* Ask for Node 1's chain, notice that it doesn't yet have Node 0's new block in it.
* Now we need Node 1 to update its chain. Ask Node 1 to resolve its chain. You'll see a response saying that Node 1's chain has been replaced.
* Ask Node 1 for its chain with a request. You'll see that it has the updated chain.
* Play around!

## What can we implement next??
* Wallets/ability to sign transactions
* Automatic block broadcast
* Ability to run nodes on other machines and have them communicate (ngrok?)
