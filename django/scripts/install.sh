#!/bin/bash
#
# Script to install python dependencies
#
# May 2017 - yogaraja.gopal@specsavers.com - Created
#
PIP_DIR=/usr/local/bin/pip3
TODAY="$(date +%Y-%m-%d_%H%M%S)"
BACKUP_DIR=/tmp
INIT_OUT=/export/ect/init.out

#-------------------------------------------------------
# Write the Log file
#-------------------------------------------------------
function log()
{
	echo "${TODAY}: $@"
	echo "${TODAY}: $@" >> ${INIT_OUT}
}
function installPython(){
	DESTINATION='/usr/local/python3.5'
	if [ ! -d $DESTINATION ]; then
		mkdir -p /usr/local/python3.5
	fi
    python3_5=`python3.5 -V 2>/dev/null | awk '{ print $2 }' | wc -l`
	if [ $python3_5 -ne 1 ]; then
	    log "Installing python3.5"
	    curl -k -L "https://buildrepo.uk.specsavers.com/nexus/service/local/repositories/releases/content/org/python/python/3.5/python-3.5.tar.xz" | tar -xzvf - -C /usr/local/python3.5/ --strip-components=1
	    cd /usr/local/python3.5
	    ./configure
	    make altinstall
	fi
}
#-------------------------------------------------------
# Install module Dependencies
#-------------------------------------------------------
function installDependentModules(){
    cd /export/ect/lib/
    log "Installing Flask module"
    ${PIP_DIR} install --no-index --find-links=file:///export/ect/lib/ ./Flask-0.12.tar.gz

    log "Installing Flask Bootstrap"
    ${PIP_DIR} install --no-index --find-links=file:///export/ect/lib/ ./Flask-Bootstrap-3.3.7.1.tar.gz

    log "Installing Flask WTF"
    ${PIP_DIR} install --no-index --find-links=file:///export/ect/lib/ ./Flask-WTF-0.14.2.tar.gz

    log "Installing Flask login"
    ${PIP_DIR} install --no-index --find-links=file:///export/ect/lib/ ./Flask-Login-0.4.0.tar.gz

    log "Installing Flask-SQLAlchemy"
    ${PIP_DIR} install --no-index --find-links=file:///export/ect/lib/ ./Flask-SQLAlchemy-2.2.tar.gz

    log "Installing Requests module"
    ${PIP_DIR} install --no-index --find-links=file:///export/ect/lib/ ./requests-2.13.0.tar.gz
}
#-------------------------------------------------------
# Main Function starts here
#-------------------------------------------------------
log "Checking if Python 3.5 is installed"
installPython
log "Starting ECT Post Upgrade Script"
installDependentModules
log "Restarting the ECT Web Application"
service ect restart

