.. default-role:: code

##################################
 Resolution patcher for Anno 1503
##################################

A simple Python script which patches the game “Anno 1503” to run at higher
resolutions.  To do so it has to replace one of the available default
resolutions.

.. image:: https://user-images.githubusercontent.com/4954650/230197537-ea73cabc-6a77-4502-9946-8dbddab6b248.png
   :alt: Screenshot of the game running at a resolution of 1600 by 900


Running
#######

You need Python 3 to run the script.  I have tested it with Python 3.11, but it
should run on 3.9 or higher as well.  There are no additional dependencies for
running.

Here is an example invocation on Unix with the game installed through `Wine`_:

.. code:: sh

   # Patch the game to the default resolution 1600x900 in current directory
   ./anno-1503-resolution-patcher.py

   # Specify resolution and game path explicitly
   ./anno-1503-resolution-patcher.py -x 1600 -y 900 '~/.wine/drive_c/GOG Games/Anno 1503 AD'

   # To see full instructions and a list of know working resolutions run this
   ./anno-1503-resolution-patcher.py --help

The patcher should work on Windows as well, but I have not been able to try it
out.  Running the script will produce one or more patched DLL files and a
patched text file.  You have to swap out the files yourself.  Only one patched
DLL file will actually work.  Here are the files which will be patched and need
to be replaced:

- `AnnoFrame.dll`
- `Texte.dat`

Why it is so complicated
========================

The script is looking for a byte pattern which matches the existing resolution.
However, there can be multiple matches for the pattern and the offset in the
DLL varies depending on which build of the game you have.  Therefore it is
impossible (at least with this naive approach) to know which patten is the one
to replace.  I took the safe route of creating all possible replacements and
offloading the verification work onto the user.

If anyone can figure out a more reliable way please let me know.

How it works
============

See the comment at the bottom of the source code.


License
#######

Released under the `MIT-0` license.  See the `LICENSE`_ file for details.  This
is as close to a “Do whatever you want” license as it gets.  This code exists
primarily for posterity and reproducibility.


Acknowledgement
###############

A patched DLL was provided by user millimarg from the `Annozone`_ forums.  In a
subsequent `post`_ he explained how he created the patch, albeit in German. I
have created this patcher script for posterity, both to document how it works
and to provide a reproducible method of creating your own patch in case the
download to the original patch ever gets lost.

I implore all hackers, modders and reverse engineers to please document your
findings and publish your source code under a Free and Open Source license.
Ready-made downloads are nice and convenient, but they will eventually fail.
Only documentation and source code (in English) are forever. Even if the code
becomes stale and stops compiling someone can still updated and restore it.  A
dead link is lost forever.


.. _LICENSE: LICENSE.txt
.. _Wine: https://www.winehq.org/
.. _Annozone: https://www.annozone.de/
.. _post: https://www.annozone.de/forum/index.php?page=Thread&postID=274837#post274837
