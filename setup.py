from distutils.core import setup

setup(
    name = "obquit",
    version = "0.2.2",
    author = "Dino Duratović",
    author_email = "dinomol@mail.com",
    url = "https://github.com/dglava/obquit",
    description = "Openbox logout script",
    license = "GNU GPLv3",

    packages = ["obquit"],
    scripts = ["bin/obquit"],
    data_files = [("/etc/obquit", ["data/obquit.conf"])]
    )
