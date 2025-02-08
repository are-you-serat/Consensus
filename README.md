## Introduction
I had the task of finding Tor bridges and checking their functionality automatically since almost all Internet resources are blocked in my country, but I did not find a tool on Github that could do all the actions for me (maybe I was looking poorly). After that I decided to write this script myself. Perhaps this script is the only one that performs this task.

Currently the following functions are available:

1) Parsing and checking DOH servers.
2) Parsing and checking vanilla bridges for Tor.
3) Parsing and checking obfs4 bridges for Tor.

The program also provides the ability to parse and check bridges from a file that was not deleted after the last scan. This is done so that it is possible to find new servers in case the site from which the data is parsed is blocked.

## Installation
1) To start, clone the repository.
2) Click on install.bat which will create a virtual environment and install dependencies.
3) After that, just click on run.bat.
