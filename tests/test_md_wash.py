
# -*- coding: utf-8 -*-

from md_wash import md_wash

def test_run_openssl_command() -> None:
    assert 1 == 1


def test_feed():
    assert 4 == md_wash.feed(2)
