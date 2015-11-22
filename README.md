# CapstoneTeamG

## Getting set up for development

Before anything else, you need to have Python up and running.

* On Ubuntu Linux, run `apt-get install python3 python3-pip`.
* On OS X, install [Homebrew](http://brew.sh), then `brew install python3`.
* On Windows, install [Chocolately](https://chocolatey.org), then `choco install python3`. Beware of possible executable name conflicts with python2, as noted on the [package description](https://chocolatey.org/packages/python3). By default the executable to use for the instructions below is is `pip.exe` and not `pip3.exe`.

Once `python3` and `pip3` are ready, run `pip3 install virtualenv`.

Once Python, pip, and virtualenv are ready, in the the `CapstoneTeamG` folder, run `virtualenv venv --python=python3.5`. This will create a `venv` subfolder to contain Python binaries, installed dependencies, etc.

Before you run any scripts in/on the project folder, you should run in the same terminal:

* bash/zsh: `source venv/bin/activate`
* csh: `source venv/bin/activate.csh`
* fish: `source venv/bin/activate.fish`
* Windows: `venv\Scripts\activate`

For initial setup, run the following. (Running `python` instead of `pip` directly here avoids some errors that can be caused by spaces in file paths.)

```shell
python venv/bin/pip install pip-tools
python venv/bin/pip install -r requirements.txt --allow-all-external
```

## Changing project requirements

After any changes to `requirements.in`, run the activate script as noted in the [README](README.md), then:

```shell
pip-compile requirements.in
pip install -r requirements.txt --allow-all-external
```
