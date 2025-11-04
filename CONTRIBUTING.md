# Contributing to DOF chat

##### Prerequisites:

1. Make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) installed.
2. Make sure you have [gh](https://github.com/cli/cli#installation) installed.

#### 1. Create the fork on GitHub, clone it locally, and wire remotes correctly.

###### Autoconfigure the remotes(origin[your fork = your_github_username/CodeandoGuadalajara/dof-chat, upstream[original repo = /dof-chat]).

```bash
gh repo fork CodeandoGuadalajara/dof-chat --clone --remote
```

#### 2. Move into the new project directory.

```bash
cd dof-chat
```

#### 3. Fetch the latest changes from upstream.

```bash
git fetch upstream
```

#### 4. Create and switch to a new feature branch starting from upstream/main.

```bash
git switch -c your-new-branch-name upstream/main
```

#### 5. Update the project's environment (ensures that all project dependencies are installed and up-to-date with the lockfile).

```bash
uv sync --frozen 
```

#### 6. Configure your IDE with the uv environment:

###### 1. VS Code (macOS, Linux, Windows):

> 1. Open the project folder (dof-chat) in VS Code.
> 2. Open the Command Palette (Cmd+Shift+P on macOS, Ctrl+Shift+P on Windows/Linux) → “Python: Select Interpreter”.
> 3. Choose “Enter interpreter path…”, paste the path to `.venv/bin/python`, and press Enter.
> 4. If .venv appears, select it. If not, choose Enter interpreter path… and use:
>     - macOS/Linux: ./.venv/bin/python
>     - Windows: .\.venv\Scripts\python.exe

###### 2. PyCharm (macOS, Linux, Windows):

> 1. Open the project folder (dof-chat) in PyCharm → Settings → Python → Interpreter → "Add Interpreter"
>    → "Add Local Interpreter" → "select existing" → "select existing" → "select existing":
>    - "Type": `uv`.
>    - "Path to uv": `$ which uv`
>    - "uv env use": `<project>/dof-chat/.venv/bin/python`.
> 2. Click OK/Apply. More details: https://www.jetbrains.com/help/pycharm/uv.html


#### 7. Make a single commit that includes your tracked file changes with a clear message.

```bash
git commit -am "<type>(<optional scope>): <description><optional body><optional footer>"
```

For more info, see: [Conventional Commits Cheatsheet](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13)

#### 8. Push your branch to your fork and set the remote tracking.

```bash
git push -u origin your-new-branch-name
```

#### 9. Open a Pull Request back to CodeandoGuadalajara/dof-chat with a prefilled title and body (edit as needed).

```bash
gh pr create --fill --repo CodeandoGuadalajara/dof-chat
```

## Troubleshooting

If you run into issues, try the following:

* Delete `.venv/` and run `uv venv` again to recreate the virtualenv.
* Make sure you are not accidentally activating another virtualenv in your shell startup files.
* If code changes do not seem to apply, run via `uv run <command>` (which auto-syncs), or re-run `uv sync`.
* Upgrade uv if needed: `uv self update`.
* Still stuck? File a GitHub issue with details.