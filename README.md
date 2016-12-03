# tumb-borg
A tumblr poetry uploader.

# Run
```
python tumb_borg.py <blog-identifier> <filename>
```
Will load all poems in filename and queue it on the blog given in the argument. Requires app credentials to run.

## Credentials
Your app key/ secret etc goes in a file ``app.secret.yml`` with the following keys:
 - `key`
 - `secret`
 - `callback`
