#!/usr/bin/perl

# Copyright 2016 Michael Schlenstedt, michael@loxberry.de
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##########################################################################
# Modules
##########################################################################

use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
use LWP::UserAgent;
use JSON qw( decode_json );
use Config::Simple;
use File::HomeDir;
use Cwd 'abs_path';
#use warnings;
#use strict;
#no strict "refs"; # we need it for template system

##########################################################################
# Variables
##########################################################################

our $cfg;
our $pcfg;
our $phrase;
our $namef;
our $value;
our %query;
our $lang;
our $template_title;
our $help;
our @help;
our $helptext;
our $helplink;
our $installfolder;
our $planguagefile;
our $version;
our $error;
our $saveformdata = 0;
our $output;
our $message;
our $nexturl;
our $do = "form";
my  $home = File::HomeDir->my_home;
our $psubfolder;
our $pname;
our $verbose;
our $languagefileplugin;
our $phraseplugin;
our $stationtyp;
our $selectedstationtyp1;
our $selectedstationtyp2;
our $selectedstationtyp3;
our $lat;
our $long;
our $stationid;
our $wuapikey;
our $getwudata;
our $cron;
our $wulang;
our $metric;
our $sendudp;
our $udpport;
our $senddfc;
our $sendhfc;
our $var;
our $theme;
our $iconset;
our $dfc;
our $hfc;
our $wuurl;
our $ua;
our $res;
our $json;
our $urlstatus;
our $urlstatuscode;
our $decoded_json;
our $query;
our $querystation;
our $found;
our $i;
our $emu;
our $emuwarning;
our $checkdnsmasq;

##########################################################################
# Read Settings
##########################################################################

# Version of this script
$version = "0.0.9";

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");

#########################################################################
# Parameter
#########################################################################

# Everything from URL
foreach (split(/&/,$ENV{'QUERY_STRING'}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# Set parameters coming in - get over post
if ( !$query{'saveformdata'} ) { 
	if ( param('saveformdata') ) { 
		$saveformdata = quotemeta(param('saveformdata')); 
	} else { 
		$saveformdata = 0;
	} 
} else { 
	$saveformdata = quotemeta($query{'saveformdata'}); 
}
#if ( !$query{'lang'} ) {
#	if ( param('lang') ) {
#		$lang = quotemeta(param('lang'));
#	} else {
#		$lang = "de";
#	}
#} else {
#	$lang = quotemeta($query{'lang'}); 
#}
if ( !$query{'do'} ) { 
	if ( param('do')) {
		$do = quotemeta(param('do'));
	} else {
		$do = "form";
	}
} else {
	$do = quotemeta($query{'do'});
}

# Clean up saveformdata variable
$saveformdata =~ tr/0-1//cd;
$saveformdata = substr($saveformdata,0,1);

# Init Language
# Clean up lang variable
$lang =~ tr/a-z//cd;
$lang = substr($lang,0,2);

# If there's no language phrases file for choosed language, use german as default
if (!-e "$installfolder/templates/plugins/$psubfolder/$lang/language.dat") {
	$lang = "de";
}

# Read translations / phrases
$planguagefile	= "$installfolder/templates/plugins/$psubfolder/$lang/language.dat";
$pphrase = new Config::Simple($planguagefile);

##########################################################################
# Main program
##########################################################################

if ($saveformdata) {
  &save;

} else {
  &form;

}

exit;

#####################################################
# 
# Subroutines
#
#####################################################

#####################################################
# Form-Sub
#####################################################

sub form {

	$pcfg             = new Config::Simple("$installfolder/config/plugins/$psubfolder/wu4lox.cfg");
	$stationtyp       = $pcfg->param("SERVER.STATIONTYP");
	$wuapikey         = $pcfg->param("SERVER.WUAPIKEY");
	$stationid        = $pcfg->param("SERVER.STATIONID");
	$coordlat         = $pcfg->param("SERVER.COORDLAT");
	$coordlong        = $pcfg->param("SERVER.COORDLONG");
	$getwudata        = $pcfg->param("SERVER.GETWUDATA");
	$cron             = $pcfg->param("SERVER.CRON");
	$wulang           = $pcfg->param("SERVER.WULANG");
	$metric           = $pcfg->param("SERVER.METRIC");
	$sendudp          = $pcfg->param("SERVER.SENDUDP");
	$udpport          = $pcfg->param("SERVER.UDPPORT");
	$senddfc          = $pcfg->param("SERVER.SENDDFC");
	$sendhfc          = $pcfg->param("SERVER.SENDHFC");
	$emu              = $pcfg->param("SERVER.EMU");
	$theme            = $pcfg->param("WEB.THEME");
	$iconset          = $pcfg->param("WEB.ICONSET");

	# Filter
	$stationtyp = quotemeta($stationtyp);
	
	# Prepare form defaults
	# STATIONTYP
	if ($stationtyp eq "statid") {
	  $selectedstationtyp1 = "checked=checked";
	} elsif ($stationtyp eq "coord") {
	  $selectedstationtyp2 = "checked=checked";
	} elsif ($stationtyp eq "autoip") {
	  $selectedstationtyp3 = "checked=checked";
	} else {
	  $selectedstationtyp1 = "checked=checked";
	} 
	# GETWUDATA
	if ($getwudata eq "1") {
	  $selectedgetwudata2 = "selected=selected";
	} else {
	  $selectedgetwudata1 = "selected=selected";
	} 
	# WULANG
	if ($wulang eq "DL") {
	  $selectedwulang1 = "selected=selected";
	} elsif ($wulang eq "EN") {
	  $selectedwulang2 = "selected=selected";
	} else {
	  $selectedwulang1 = "selected=selected";
	} 
	# METRIC
	if ($metric eq "1") {
	  $selectedmetric1 = "selected=selected";
	} else {
	  $selectedmetric2 = "selected=selected";
	} 
	# CRON
	if ($cron eq "1") {
	  $selectedcron1 = "selected=selected";
	} elsif ($cron eq "3") {
	  $selectedcron2 = "selected=selected";
	} elsif ($cron eq "5") {
	  $selectedcron3 = "selected=selected";
	} elsif ($cron eq "10") {
	  $selectedcron4 = "selected=selected";
	} elsif ($cron eq "15") {
	  $selectedcron5 = "selected=selected";
	} elsif ($cron eq "30") {
	  $selectedcron6 = "selected=selected";
	} elsif ($cron eq "60") {
	  $selectedcron7 = "selected=selected";
	} else {
	  $selectedcron2 = "selected=selected";
	}
	# SENDUDP
	if ($sendudp eq "1") {
	  $selectedsendudp2 = "selected=selected";
	} else {
	  $selectedsendudp1 = "selected=selected";
	} 
	# DFC
	foreach (split(/;/,$senddfc)){
		$var ="selecteddfc$_";
		${$var} = "checked=checked";
	}
	# HFC
	foreach (split(/;/,$sendhfc)){
		$var ="selectedhfc$_";
		${$var} = "checked=checked";
	}
	# THEME
	if ($theme eq "classic") {
	  $selectedtheme1 = "selected=selected";
	} elsif ($theme eq "appv4") {
	  $selectedtheme2 = "selected=selected";
	} elsif ($theme eq "custom") {
	  $selectedtheme3 = "selected=selected";
	} else {
	  $selectedtheme2 = "selected=selected";
	}
	# ICONSET
	if ($iconset eq "color") {
	  $selectediconset1 = "selected=selected";
	} elsif ($iconset eq "flat") {
	  $selectediconset2 = "selected=selected";
	} elsif ($iconset eq "dark") {
	  $selectediconset3 = "selected=selected";
	} elsif ($iconset eq "light") {
	  $selectediconset4 = "selected=selected";
	} elsif ($iconset eq "green") {
	  $selectediconset5 = "selected=selected";
	} elsif ($iconset eq "silver") {
	  $selectediconset6 = "selected=selected";
	} elsif ($iconset eq "realistic") {
	  $selectediconset7 = "selected=selected";
	} elsif ($iconset eq "custom") {
	  $selectediconset8 = "selected=selected";
	} else {
	  $selectediconset4 = "selected=selected";
	}
	# EMU
	if ($emu eq "1") {
	  $selectedemu2 = "selected=selected";
	} else {
	  $selectedemu1 = "selected=selected";
	} 

        # Check for installed DNSMASQ-Plugin
        $checkdnsmasq = `cat $home/data/system/plugindatabase.dat | grep -c -i DNSmasq`;
	if ($checkdnsmasq > 0) {
          $emuwarning = $pphrase->param("TXT0007");
	}

	print "Content-Type: text/html\n\n";
	
	$template_title = $pphrase->param("TXT0000") . ": " . $pphrase->param("TXT0001");
	
	# Print Template
	&lbheader;
	open(F,"$installfolder/templates/plugins/$psubfolder/$lang/settings.html") || die "Missing template plugins/$psubfolder/$lang/settings.html";
	  while (<F>) 
	  {
	    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
	    print $_;
	  }
	close(F);
	&footer;

	exit;

}

#####################################################
# Save-Sub
#####################################################

sub save 
{

	# Read Config
	$pcfg    = new Config::Simple("$installfolder/config/plugins/$psubfolder/wu4lox.cfg");
	$wuurl   = $pcfg->param("SERVER.WUURL");
	$pname   = $pcfg->param("PLUGIN.SCRIPTNAME");

	# Everything from Forms
	$apikey     = param('apikey');
	$stationtyp = param('stationtyp');
	$stationid  = param('stationid');
	$coordlat   = param('coordlat');
	$coordlong  = param('coordlong');
	$wulang     = param('wulang');
	$metric     = param('metric');
	$getwudata  = param('getwudata');
	$emu        = param('emu');
	$cron       = param('cron');
	$sendudp    = param('sendudp');
	$udpport    = param('udpport');
	$theme      = param('theme');
	$iconset    = param('iconset');
	for ($i=1;$i<=4;$i++) {
		if ( param("dfc$i") &&  param("dfc$i") ne "0" &&  param("dfc$i") ne "" ) {
			if ($i eq "1") {
				$dfc = $i;
			} else {
				$dfc = $dfc . ";" . $i;
			}
		}
	}
	for ($i=1;$i<=36;$i++) {
		if ( param("hfc$i") &&  param("hfc$i") ne "0" &&  param("hfc$i") ne "" ) {
			if ($i eq "1") {
				$hfc = $i;
			} else {
				$hfc = $hfc . ";" . $i;
			}
		}
	}
	
	# Filter
	$wuapikey   = quotemeta($apikey);
	$stationtyp = quotemeta($stationtyp);
	#$stationid = quotemeta($stationid);
	#$coordlat   = quotemeta($coordlat);
	#$coordlong  = quotemeta($coordlong);
	$wulang     = quotemeta($wulang);
	$metric     = quotemeta($metric);
	$getwudata  = quotemeta($getwudata);
	$emu        = quotemeta($emu);
	$cron       = quotemeta($cron);
	$sendudp    = quotemeta($sendudp);
	$udpport    = quotemeta($udpport);
	#$dfc        = quotemeta($dfc);
	#$hfc        = quotemeta($hfc);
	$theme      = quotemeta($theme);
	$iconset    = quotemeta($iconset);

	# Check for Station
	if ($stationtyp eq "statid") {
		$querystation = $stationid;
	} 
	elsif ($stationtyp eq "coord") {
		$querystation = $coordlat . "," .$coordlong;
	}
	else {
		$querystation = "autoip";
	}

	# 1. attempt to query Wunderground
	&wuquery;

	$found = 0;
	if ( $decoded_json->{current_observation}->{station_id} ) {
		$found = 1;
	}
	if ( !$found && $decoded_json->{response}->{error}->{type} eq "keynotfound" ) {
		$error = $pphrase->param("TXT0004") . "<br><br><b>WU Error Message:</b> $decoded_json->{response}->{error}->{description}";
		&error;
		exit;
	}

	# 2. attempt to query Wunderground
	# Before giving up test if it is a PWS
	if (!$found) {
		$querystation = "pws:$querystation";
		&wuquery;
		if ( $decoded_json->{current_observation}->{station_id} ) {
			$found = 1;
		}
	}

	# 3. attempt to query Wunderground
	# Before giving up test if it is a ZMW
	if (!$found) {
		$querystation = "zmw:$querystation";
		&wuquery;
		if ( $decoded_json->{current_observation}->{station_id} ) {
			$found = 1;
		}
	}

	# That was my last attempt - if we haven't found the station, we are giving up.
	if (!$found) {
		$error = $pphrase->param("TXT0005");
		&error;
		exit;
	}

	# OK - now installing...

	# Write configuration file(s)
	$pcfg->param("SERVER.WUAPIKEY", "$wuapikey");
	$pcfg->param("SERVER.STATIONTYP", "$stationtyp");
	$pcfg->param("SERVER.STATIONID", "\"$querystation\"");
	$pcfg->param("SERVER.COORDLAT", "$coordlat");
	$pcfg->param("SERVER.COORDLONG", "$coordlong");
	$pcfg->param("SERVER.GETWUDATA", "$getwudata");
	$pcfg->param("SERVER.CRON", "$cron");
	$pcfg->param("SERVER.METRIC", "$metric");
	$pcfg->param("SERVER.WULANG", "$wulang");
	$pcfg->param("SERVER.SENDDFC", "$dfc");
	$pcfg->param("SERVER.SENDHFC", "$hfc");
	$pcfg->param("SERVER.SENDUDP", "$sendudp");
	$pcfg->param("SERVER.UDPPORT", "$udpport");
	$pcfg->param("SERVER.EMU", "$emu");
	$pcfg->param("WEB.THEME", "$theme");
	$pcfg->param("WEB.ICONSET", "$iconset");

	$pcfg->save();
		
	# Create Cronjob
	if ($getwudata eq "1") 
	{
	  if ($cron eq "1") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.01min/$pname");
	    unlink ("$installfolder/system/cron/cron.03min/$pname");
	    unlink ("$installfolder/system/cron/cron.05min/$pname");
	    unlink ("$installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.30min/$pname");
	    unlink ("$installfolder/system/cron/cron.hourly/$pname");
	  }
	  if ($cron eq "3") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.03min/$pname");
	    unlink ("$installfolder/system/cron/cron.01min/$pname");
	    unlink ("$installfolder/system/cron/cron.05min/$pname");
	    unlink ("$installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.30min/$pname");
	    unlink ("$installfolder/system/cron/cron.hourly/$pname");
	  }
	  if ($cron eq "5") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.05min/$pname");
	    unlink ("$installfolder/system/cron/cron.01min/$pname");
	    unlink ("$installfolder/system/cron/cron.03min/$pname");
	    unlink ("$installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.30min/$pname");
	    unlink ("$installfolder/system/cron/cron.hourly/$pname");
	  }
	  if ($cron eq "10") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.1min/$pname");
	    unlink ("$installfolder/system/cron/cron.3min/$pname");
	    unlink ("$installfolder/system/cron/cron.5min/$pname");
	    unlink ("$installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.30min/$pname");
	    unlink ("$installfolder/system/cron/cron.hourly/$pname");
	  }
	  if ($cron eq "15") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.01min/$pname");
	    unlink ("$installfolder/system/cron/cron.03min/$pname");
	    unlink ("$installfolder/system/cron/cron.05min/$pname");
	    unlink ("$installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.30min/$pname");
	    unlink ("$installfolder/system/cron/cron.hourly/$pname");
	  }
	  if ($cron eq "30") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.30min/$pname");
	    unlink ("$installfolder/system/cron/cron.01min/$pname");
	    unlink ("$installfolder/system/cron/cron.03min/$pname");
	    unlink ("$installfolder/system/cron/cron.05min/$pname");
	    unlink ("$installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.hourly/$pname");
	  }
	  if ($cron eq "60") 
	  {
	    system ("ln -s $installfolder/webfrontend/cgi/plugins/$psubfolder/bin/fetch.pl $installfolder/system/cron/cron.hourly/$pname");
	    unlink ("$installfolder/system/cron/cron.01min/$pname");
	    unlink ("$installfolder/system/cron/cron.03min/$pname");
	    unlink ("$installfolder/system/cron/cron.05min/$pname");
	    unlink ("$installfolder/system/cron/cron.10min/$pname");
	    unlink ("$installfolder/system/cron/cron.15min/$pname");
	    unlink ("$installfolder/system/cron/cron.30min/$pname");
	  }
	} 
	else
	{
	  unlink ("$installfolder/system/cron/cron.01min/$pname");
	  unlink ("$installfolder/system/cron/cron.03min/$pname");
	  unlink ("$installfolder/system/cron/cron.05min/$pname");
	  unlink ("$installfolder/system/cron/cron.10min/$pname");
	  unlink ("$installfolder/system/cron/cron.15min/$pname");
	  unlink ("$installfolder/system/cron/cron.30min/$pname");
	  unlink ("$installfolder/system/cron/cron.hourly/$pname");
	}

	$template_title = $pphrase->param("TXT0000") . " - " . $pphrase->param("TXT0001");
	$message = $pphrase->param("TXT0006");
	$nexturl = "./index.cgi?do=form";

	print "Content-Type: text/html\n\n"; 
	&lbheader;
	open(F,"$installfolder/templates/system/$lang/success.html") || die "Missing template system/$lang/error.html";
	while (<F>) 
	{
		$_ =~ s/<!--\$(.*?)-->/${$1}/g;
		print $_;
	}
	close(F);
	&footer;
	exit;
		
}

#####################################################
# Query Wunderground
#####################################################

sub wuquery
{

        # Get data from Wunderground Server (API request) for testing API Key and Station
        $query = "$wuurl\/$wuapikey\/conditions\/pws:1\/lang:EN\/q\/$querystation\.json";

        $ua = new LWP::UserAgent;
        $res = $ua->get($query);
        $json = $res->decoded_content();

        # Check status of request
        $urlstatus = $res->status_line;
        $urlstatuscode = substr($urlstatus,0,3);

        if ($urlstatuscode ne "200") {
                $error = $pphrase->param("TXT0003") . "<br><br><b>URL:</b> $query<br><b>STATUS CODE:</b> $urlstatuscode";
                &error;
                exit;
        }

        # Decode JSON response from server
        $decoded_json = decode_json( $json );

	return();

}

#####################################################
# Error-Sub
#####################################################

sub error 
{
	$template_title = $pphrase->param("TXT0000") . " - " . $pphrase->param("TXT0001");
	print "Content-Type: text/html\n\n"; 
	&lbheader;
	open(F,"$installfolder/templates/system/$lang/error.html") || die "Missing template system/$lang/error.html";
	while (<F>) 
	{
		$_ =~ s/<!--\$(.*?)-->/${$1}/g;
		print $_;
	}
	close(F);
	&footer;
	exit;
}

#####################################################
# Page-Header-Sub
#####################################################

	sub lbheader 
	{
		 # Create Help page
	  $helplink = "http://www.loxwiki.eu:80/x/uYCm";
	  open(F,"$installfolder/templates/plugins/$psubfolder/$lang/help.html") || die "Missing template plugins/$psubfolder/$lang/help.html";
	    @help = <F>;
	    foreach (@help)
	    {
	      s/[\n\r]/ /g;
	      $_ =~ s/<!--\$(.*?)-->/${$1}/g;
	      $helptext = $helptext . $_;
	    }
	  close(F);
	  open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
	    while (<F>) 
	    {
	      $_ =~ s/<!--\$(.*?)-->/${$1}/g;
	      print $_;
	    }
	  close(F);
	}

#####################################################
# Footer
#####################################################

	sub footer 
	{
	  open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/footer.html";
	    while (<F>) 
	    {
	      $_ =~ s/<!--\$(.*?)-->/${$1}/g;
	      print $_;
	    }
	  close(F);
	}
