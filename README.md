Simple docker image to switch role to another account.

Usage:

    eval "$( docker run -i -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN  \
        mergermarket/switch-role --account accountname --role-name admin --role-session-name $EMAIL \
    )"
