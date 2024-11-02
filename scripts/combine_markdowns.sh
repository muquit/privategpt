#!/bin/sh
########################################################################
# Combine markdown files from ./markdowns directory to create README.md
# with markdown_helper ruby gem
# muquit@muquit.com Oct-12-2024 
########################################################################
MH="markdown_helper"
RM="/bin/rm -f"
MDIR="./markdowns"

update_config_md() {
    local -r f="${MDIR}/config.md"
    local -r cf="./config.py"
    echo "# Configuration file" > ${f}
    echo "Please update as needed" >> ${f}
    echo "" >> ${f}
    while IFS= read -r line; do
        echo "    $line" >> ${f}
    done < "${cf}"
}

update_version_md() {
    local -r VERSION=$(grep "VERSION=" config.py | cut -d'"' -f2)
    local -r f=${MDIR}/version.md
    cat << EOF > ${f}
# Version

The current version of the tools is ${VERSION}.

Please look at [ChangeLog](ChangeLog.md) for what has changed in the
current version.  It is possible, new python modules need to be installed.
EOF
}

update_license() {
    local -r f="${MDIR}/license.md"
    local -r lf="LICENSE.txt"

    echo "# License" > ${f}
    echo "" >> ${f}
    while IFS= read -r line; do
        echo "    ${line}" >> ${f}
    done < "${lf}"
}

create_cli_synopsis()
{
    local -r f=${MDIR}/cli_synopsis.md
    echo "## CLI" > ${f}
    echo "" >> $f
    echo '```' >> $f
    ./assistant/assistant_cli.py --help >> ${MDIR}/cli_synopsis.md
    echo '```' >> $f
}

update_config_md
update_license
create_cli_synopsis
update_version_md

pushd ${MDIR} >/dev/null 
echo " - Assembling README.md"
${MH} include --pristine main.md ../README.md
#${MH} include --pristine chl.md ../ChangeLog.md
popd >/dev/null
