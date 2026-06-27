# Legacy installation and uninstall

For current installation instructions see [README](README.md).

---

## Symlink method (deprecated)

The previous installation method involved cloning the repo and creating
a symlink manually:

```bash
mkdir -p $HOME/.myPrograms
cd $HOME/.myPrograms
ln -s /path/to/isonav/isonav.py isonav
```

Then adding the following to your `.bashrc` or `.zshrc`:

```bash
export PATH=$PATH:$HOME/.myPrograms
```

To uninstall, remove the symlink and the `export` line from your rc file:

```bash
rm $HOME/.myPrograms/isonav
```

This method was replaced by the Homebrew and PyPI distributions, which
handle dependencies automatically and don't require manual path management.

---

## installScript.sh method (deprecated)

The installScript.sh procedure was deprecated because it required root
privileges — something a user doesn't always have. Additionally, getting
the database set up was fragile. The DB has since been committed directly
to the repo (it's small and rarely changes), favoring practicality over
the strict "good practices" the old method tried to enforce.

To uninstall a legacy installScript.sh installation, run:

```bash
sudo ./uninstallLegacy.sh
```

If you are on a Mac and get an "Operation not permitted" error, you may
need to temporarily disable System Integrity Protection: reboot pressing
Cmd-R, open a terminal and run `csrutil disable`, reboot, run the
uninstall script, then re-enable it with `csrutil enable`.
