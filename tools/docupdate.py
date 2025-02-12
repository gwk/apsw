# python
#
# See the accompanying LICENSE file.
#
# various automagic documentation updates

import sys

# get the download file names correct

version = sys.argv[1]
url = "  <https://github.com/rogerbinns/apsw/releases/download/" + version + "/%s>`__"
version_no_r = version.split("-r")[0]


download = open("doc/download.rst", "rt").read()


op = []
incomment = False
for line in open("doc/download.rst", "rt"):
    line = line.rstrip()
    if line == ".. downloads-begin":
        op.append(line)
        incomment = True
        op.append("")
        op.append("* `apsw-%s.zip" % (version, ))
        op.append(url % ("apsw-%s.zip" % version))
        op.append("  (Source, includes this HTML Help)")
        op.append("")
        op.append("* `apsw-%s-sigs.zip " % (version, ))
        op.append(url % ("apsw-%s-sigs.zip" % version))
        op.append("  GPG signatures for all files")
        op.append("")
        continue
    if line == ".. downloads-end":
        incomment = False
    if incomment:
        continue
    if line.lstrip().startswith("$ gpg --verify apsw"):
        line = line[:line.index("$")] + "$ gpg --verify apsw-%s.zip.asc" % (version, )
    op.append(line)

op = "\n".join(op)
if op != download:
    open("doc/download.rst", "wt").write(op)

# put usage and description for speedtest into benchmark

import apsw.speedtest

benchmark = open("doc/benchmarking.rst", "rt").read()

op = []
incomment = False
for line in open("doc/benchmarking.rst", "rt"):
    line = line.rstrip()
    if line == ".. speedtest-begin":
        op.append(line)
        incomment = True
        op.append("")
        op.append(".. code-block:: text")
        op.append("")
        op.append("    $ python3 -m apsw.speedtest --help")
        apsw.speedtest.parser.set_usage("Usage: apsw.speedtest [options]")
        for line in apsw.speedtest.parser.format_help().split("\n"):
            op.append("    " + line)
        op.append("")
        op.append("    $ python3 -m apsw.speedtest --tests-detail")
        for line in apsw.speedtest.tests_detail.split("\n"):
            op.append("    " + line)
        op.append("")
        continue
    if line == ".. speedtest-end":
        incomment = False
    if incomment:
        continue
    op.append(line)

op = "\n".join(op)
if op != benchmark:
    open("doc/benchmarking.rst", "wt").write(op)

# shell stuff

import apsw, io, apsw.shell
shell = apsw.shell.Shell()
incomment = False
op = []
for line in open("doc/shell.rst", "rt"):
    line = line.rstrip()
    if line == ".. help-begin:":
        op.append(line)
        incomment = True
        op.append("")
        op.append(".. code-block:: text")
        op.append("")
        s = io.StringIO()

        def tw(*args):
            return 80

        shell.stderr = s
        shell._terminal_width = tw
        shell.command_help([])
        op.extend(["  " + x for x in s.getvalue().split("\n")])
        op.append("")
        continue
    if line == ".. usage-begin:":
        op.append(line)
        incomment = True
        op.append("")
        op.append(".. code-block:: text")
        op.append("")
        op.extend(["  " + x for x in shell.usage().split("\n")])
        op.append("")
        continue
    if line == ".. help-end:":
        incomment = False
    if line == ".. usage-end:":
        incomment = False
    if incomment:
        continue
    op.append(line)

op = "\n".join(op)
if op != open("doc/shell.rst", "rt").read():
    open("doc/shell.rst", "wt").write(op)
