#!/bin/sh

branch="$(git rev-parse --abbrev-ref HEAD)"

if [ "$branch" = "main" ]; then
  echo "Main Branch commit is blocked"
  exit 1
fi

if [ "$branch" = "staging" ]; then
  echo "Staging Branch commit is blocked"
  exit 1
fi

exit 0
