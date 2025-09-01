#!/usr/bin/env python3
"""
Usage:
  python main.py         # launches the User login (default)
  python main.py --admin # launches the Admin dashboard
  python main.py --user  # explicitly launch User login
"""
import sys, subprocess, importlib

def _first_exists(names):
    for mod in names:
        try:
            importlib.import_module(mod)
            return mod
        except ModuleNotFoundError:
            pass
    return None

def _run(modname):
    subprocess.run([sys.executable, "-m", modname], check=False)

if __name__ == "__main__":
    # works whether your irrespetive of the folder
    user_mod  = _first_exists(["user.LoginUser",  "User.LoginUser",  "user.Home",  "User.Home"])
    admin_mod = _first_exists(["admin.admin_dashboard", "Admin.admin_dashboard"])

    # pick target
    target = user_mod
    if "--admin" in sys.argv: target = admin_mod
    if "--user"  in sys.argv: target = user_mod

    if not target:
        print("Couldn't find the start module. Make sure 'user/' and 'admin/' (or 'User/'/'Admin/') contain __init__.py.")
        sys.exit(1)

    _run(target)
