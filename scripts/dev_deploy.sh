#!/bin/bash
# adapted from http://blog.abarbanell.de/linux/2017/09/09/deploy-from-travis-to-dokku/
echo "$SSH_PRIVATE_KEY" >> deploy_key
chmod 600 deploy_key
eval "$(ssh-agent -s)"
ssh-add deploy_Key
ssh-keyscan tessera-dev.haydenwoodhead.com >> >> ~/.ssh/known_hosts
git remote add deploy dokku@tessera-dev.haydenwoodhead.com:dev-api
git config --global push.default simple
git push deploy dev:master