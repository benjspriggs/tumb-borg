# tumb-borg
A tumblr poetry uploader.

## Run
```
python tumb_borg.py <blog-identifier> <filename>
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
