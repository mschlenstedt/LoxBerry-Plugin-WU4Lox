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
