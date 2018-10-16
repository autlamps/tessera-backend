#!/bin/bash
# adapted from http://blog.abarbanell.de/linux/2017/09/09/deploy-from-travis-to-dokku/
eval "$(ssh-agent -s)"
openssl aes-256-cbc -K $encrypted_caa4193d7352_key -iv $encrypted_caa4193d7352_iv -in .travis/deploy.key.enc -out .travis/deploy.key -d
chmod 600 .travis/deploy.key
ssh-add .travis/deploy.key
echo -ne '\n' | ssh-add deploy_key
ssh-keyscan tessera-dev.haydenwoodhead.com >> ~/.ssh/known_hosts
git remote add deploy dokku@tessera-dev.haydenwoodhead.com:dev-api
git config --global push.default simple
git push --force deploy dev:master