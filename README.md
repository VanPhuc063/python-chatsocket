Installing Python with pyenv
$ pyenv install 3.7.6
Creating virtual environment
$ pyenv virtualenv 3.7.6 socketchat
Using the virtual environment
$ pyenv activate socketchat

For running the project, you will need to have an server to receive and send messages to clients that are connected, and at least 2 clients to see messages being broadcasted.

Creating the server:

If you are using Python 3.7.6 without pyenv, run the following command below to start running server:

$ python3 server.py
If you are using pyenv, just run the following command to up the server:

(socketchat) $ python server.py
Creating clients:

Now we are going to need two clients, in order to see each other message on terminal.

If you are using Python 3.7.6 without pyenv, run the following command in two different terminals/bashes in order to create our clients and exchange messagens between them.

$ python3 client.py
Otherwise if you are using pyenv, simply run the following code in different terminals/bashes:

(socketchat) $ python client.py
