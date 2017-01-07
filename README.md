# tumb-borg
A tumblr poetry uploader.

## Run
```
./tumb_borg.py <blog-identifier> <filename>
```
Will load all poems in filename and queue it on the blog given in the argument.
[Requires app credentials to run](https://www.tumblr.com/docs/en/api/v2).

## Credentials
Your app key/ secret etc goes in a file ``app.secret.yml`` with the following keys:
 - `key`
 - `secret`
 - `callback`

## Setup
1. Sign up for a Tumblr account.
1. Go to <https://www.tumblr.com/docs/en/api/v2> and click 'Register an Application'.
1. Register a new application.
 - The name can be whatever you want
 - The callback url can be whatever you want, `/` will work as well (it links the callback to your dashboard)
 - The description can be whatever you want
1. Click 'Register'.
1. Copy the `OAuth Consumer Key`, `Secret Key` and save it in ``app.secret.yml``:
```yml
---
key: <OAuth Consumer Key>
secret: <Secret Key>
callback: <your callback url>
[batch-tags]: '<optional batch tags that are added to each post>'
```
### Python 2
If you are getting the following error:
```shell
ImportError: No module named builtins
```
Make sure to update future from pip:
``pip install future --upgrade``
### Ubuntu
Make sure to install the ``python3-setuptools`` and ``python3-pip`` packages from apt, if you want to use the Python 3 version of this script.
