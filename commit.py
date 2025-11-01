from git.util import Actor
from git import Repo
from pathlib import Path
import sys, os

def say(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

repo = Repo.init(".")
tree = repo.head.commit.tree

fake_me = Actor("mrtnvgr", "avoiding-commit-stats@example.com")
origin = repo.remote(name="origin")

files = list(map(str, Path(".").rglob("*")))

is_file = lambda x: not os.path.isdir(x)
files = list(filter(is_file, files))

is_new = lambda x: x in tree
files = list(filter(is_new, files))

skip_git = lambda x: not x.startswith(".git")
files = list(filter(skip_git, files))

count = len(files)
print(f"Found {count} new file(s)")

for i, file in enumerate(files):
    say(f"[{i+1}/{count}] {file}......", end="")

    repo.index.add(file)
    repo.index.commit(f"{file}: add", author = fake_me)
    origin.push()

    say("Done!")
