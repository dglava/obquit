from distutils.core import setup

setup(
    name = "obquit",
    version = "0.1.0",
    author = "Dino Duratović",
    author_email = "dinomol at mail dot com",
    url = "https://github.com/dglava/obquit",
    description = "Openbox logout script",
    license = "GNU GPLv3",

    packages = ["obquit"],
    scripts = ["bin/obquit"],
    data_files = [("/etc", ["data/obquit.conf"])]
    )
