#!/bin/bash

if [ -e $LBPLOG/REPLACELBPPLUGINDIR/current.dat ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/current.dat $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/REPLACELBPPLUGINDIR/dailyforecast.dat ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/dailyforecast.dat $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/hourlyforecast.dat ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/hourlyforecast.dat $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/hourlyhistory.dat ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/hourlyhistory.dat $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/webpage.html ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/webpage.html $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/webpage..map.html ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/webpage.map.html $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/webpage.dfc.html ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/webpage.dfc.html $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/webpage.hfc.html ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/webpage.hfc.html $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/weatherdata.html ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/weatherdata.html $LBPDATA/REPLACELBPPLUGINDIR
fi
if [ -e $LBPLOG/opt/loxberry/log/plugins/REPLACELBPPLUGINDIR/index.txt ]; then
	cp $LBPLOG/REPLACELBPPLUGINDIR/index.txt $LBPDATA/REPLACELBPPLUGINDIR
fi
