#! /usr/bin/env python

from time import sleep

import django

from events.utils import send_invites, check_for_replies


if __name__ == "__main__":
    django.setup()
    while True:
        send_invites()
        sleep(1)
        check_for_replies()
        sleep(1)
