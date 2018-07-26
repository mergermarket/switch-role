Simple docker image to switch role to another account.

Usage:

    SAVE_XTRACE_STATUS="$(set +o | grep xtrace)"; set +x
    eval "$( docker run --rm -i -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN  \
        mergermarket/switch-role --account accountname --role-name admin --role-session-name "$JOB_NAME" \
    )"
    eval "$SAVE_XTRACE_STATUS"; unset SAVE_XTRACE_STATUS

The `--role-session-name` option is required when using IAM user credentials (e.g. from Jenkins) - invalid characters are removed and truncation is applied to ensure this works.

You can also put it in a bash function to make it more readable:

    switch_role(){
        SAVE_XTRACE_STATUS="$(set +o | grep xtrace)"; set +x
        eval "$( docker run --rm -i -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN  \
            mergermarket/switch-role --account "$1" --role-name "$2" --role-session-name "$JOB_NAME" \
        )"
        eval "$SAVE_XTRACE_STATUS"; unset SAVE_XTRACE_STATUS
    }
    
    # now is more readbable:
    switch_role accountname admin
