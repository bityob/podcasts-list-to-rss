#!/bin/sh

# Decrypt the file
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$SESSION_SECRET_PASSPHRASE" \
--output user.session user.session.gpg