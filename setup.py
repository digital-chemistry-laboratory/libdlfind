#  Copyright 2021 Kjell Jorner
#
#  This file is part of libdlfind.
#
#  libdlfind is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  libdlfind is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with libdlfind.  If not, see
#  <http://www.gnu.org/licenses/>.

from skbuild import setup

URL = "https://github.com/kjelljorner/libdlfind"
DESCRIPTION = "Python library for DL-FIND"
LONG_DESCRIPTION = f"""\
{DESCRIPTION}. For more information, see the [project repository]({URL}).
"""

setup(
    name="libdlfind",
    version="0.0.2",
    author="Kjell Jorner",
    author_email="kjell.jorner@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=["libdlfind"],
    python_requires=">=3.8",
    install_requires=["numpy"],
    include_package_data=True,
    cmake_args=["-DSKBUILD=ON"],
    license="LGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
