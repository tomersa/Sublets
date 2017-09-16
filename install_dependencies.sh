#!/bin/sh
is_simple_crypt=$(pip list | grep "simple-crypt")
if ! [ "$is_simple_crypt" ]
then
  pip install simple-crypt
fi
