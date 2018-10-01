# tessera-backend
[![Build Status](https://travis-ci.org/autlamps/tessera-backend.svg?branch=master)](https://travis-ci.org/autlamps/tessera-backend)

Open source shuttle/bus ticketing system 

# Installation

1. Download project

    1. Download git project
    `git clone https://github.com/autlamps/tessera-backend.git`

    2. Move into dir
    `cd tessera-backend`
    
    3. Checkout the dev branch (or master preferably if it's available)
    `git checkout origin/dev`

2. Setup environment variables

    Assumes linux environment.

    ```
        # Django key used to sign cookies and api tokens (keep this secret)
        # Can use this website: https://www.miniwebtool.com/django-secret-key-generator/
        export KEY=$SOMESECRETKEY
        
        # Disable debug mode (absolutely do not leave debug=true in production)
        export DEBUG=False | True
        
        # Set hostname (where this api is being hosted)
        export HOSTNAME=$HOSTNAME
        
        # Database (postgres formatted db url
        export DATABASE=postgres://USER:PASSWORD@HOST:PORT/NAME
        
        # Generate public and private keys using http://travistidwell.com/jsencrypt/demo/
        # you will need to delete all newlines and ensure the key is one line only
        # Tessera-backend will parse this key correctly
        
        # Public Key
        export PUBLIC_KEY=$PUBLIC_KEY
        
        # Private Key (keep this secret)
        export PRIVATE_KEY=$PRIVATE_KEY
    ```

3. Install pip dependencies 

    `pip install -r requirements.txt`
    
4. Run gunicorn 
    
    `gunicorn -b 0.0.0.0:$PORT tessera.wsgi`


Preferably run this in docker. This is left as an exercise for the reader.

# Documentation

Once the server is setup and running api documentation can be found at $HOSTNAME/docs/


# License

Tessera-backend is licensed under the MIT license.