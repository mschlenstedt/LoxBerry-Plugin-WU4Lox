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
use CGI;
use LWP::UserAgent;
use JSON qw( decode_json );
use LoxBerry::System;
use LoxBerry::Web;
#use warnings;
#use strict;

##########################################################################
# Variables
##########################################################################

# Read Form
my $cgi = CGI->new;
$cgi->import_names('R');

##########################################################################
# Read Settings
##########################################################################

# Version of this script
my $version = LoxBerry::System::pluginversion();

# Settings
my $cfg = new Config::Simple("$lbpconfigdir/wu4lox.cfg");
my $wuurl = $cfg->param("SERVER.WUURL");

#########################################################################
# Parameter
#########################################################################

my $error;

##########################################################################
# Main program
##########################################################################

# Template
my $template = HTML::Template->new(
    filename => "$lbptemplatedir/settings.html",
    global_vars => 1,
    loop_context_vars => 1,
    die_on_bad_params => 0,
    associate => $cfg,
);

# Language
my %L = LoxBerry::Web::readlanguage($template, "language.ini");

# Save Form 1 (Wunderground)
if ($R::saveformdata1) {
	
  	$template->param( FORMNO => '1' );

	# Check for Station
	our $querystation;
	if ($R::stationtyp eq "statid") {
		$querystation = $R::stationid;
	} 
	elsif ($R::stationtyp eq "coord") {
		$querystation = $R::coordlat . "," .$R::coordlong;
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
		$error = $L{'SETTINGS.ERR_API_KEY'} . "<br><br><b>WU Error Message:</b> $decoded_json->{response}->{error}->{description}";
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
	$cfg->param("SERVER.WUAPIKEY", "$R::apikey");
	$cfg->param("SERVER.STATIONTYP", "$R::stationtyp");
	$cfg->param("SERVER.STATIONID", "\"$querystation\"");
	$cfg->param("SERVER.COORDLAT", "$R::coordlat");
	$cfg->param("SERVER.COORDLONG", "$R::coordlong");
	$cfg->param("SERVER.GETWUDATA", "$R::getwudata");
	$cfg->param("SERVER.CRON", "$R::cron");
	$cfg->param("SERVER.METRIC", "$R::metric");
	$cfg->param("SERVER.WULANG", "$R::wulang");

	$cfg->save();
		
	# Create Cronjob
	if ($R::getwudata eq "1") 
	{
	  if ($R::cron eq "1") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.01min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.03min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.05min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	  }
	  if ($R::cron eq "3") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.03min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.01min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.05min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	  }
	  if ($R::cron eq "5") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.05min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.01min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.03min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	  }
	  if ($R::cron eq "10") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.1min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.3min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.5min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	  }
	  if ($R::cron eq "15") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.01min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.03min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.05min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	  }
	  if ($R::cron eq "30") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.30min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.01min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.03min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.05min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	  }
	  if ($R::cron eq "60") 
	  {
	    system ("ln -s $lbpbindir/fetch.pl $lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.01min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.03min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.05min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	    unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	  }
	} 
	else
	{
	  unlink ("$lbhomedir/system/cron/cron.01min/$lbpplugindir");
	  unlink ("$lbhomedir/system/cron/cron.03min/$lbpplugindir");
	  unlink ("$lbhomedir/system/cron/cron.05min/$lbpplugindir");
	  unlink ("$lbhomedir/system/cron/cron.10min/$lbpplugindir");
	  unlink ("$lbhomedir/system/cron/cron.15min/$lbpplugindir");
	  unlink ("$lbhomedir/system/cron/cron.30min/$lbpplugindir");
	  unlink ("$lbhomedir/system/cron/cron.hourly/$lbpplugindir");
	}

	# Template output
	&save;

	exit;

}

# Save Form 2 (Miniserver)
if ($R::saveformdata2) {
	
  	$template->param( FORMNO => '2' );

	my $dfc;
	for (my $i=1;$i<=4;$i++) {
		if ( ${"R::dfc$i"} ) {
			if ( !$dfc ) {
				$dfc = $i;
			} else {
				$dfc = $dfc . ";" . $i;
			}
		}
	}
	my $hfc;
	for ($i=1;$i<=36;$i++) {
		if ( ${"R::hfc$i"} ) {
			if ( !$hfc ) {
				$hfc = $i;
			} else {
				$hfc = $hfc . ";" . $i;
			}
		}
	}
	
	# Write configuration file(s)
	$cfg->param("SERVER.SENDDFC", "$dfc");
	$cfg->param("SERVER.SENDHFC", "$hfc");
	$cfg->param("SERVER.SENDUDP", "$R::sendudp");
	$cfg->param("SERVER.UDPPORT", "$R::udpport");

	$cfg->save();
	
	# Template output
	&save;

	exit;

}

# Save Form 3 (Website)
if ($R::saveformdata3) {
	
  	$template->param( FORMNO => '3' );

	# Write configuration file(s)
	$cfg->param("SERVER.EMU", "$R::emu");
	$cfg->param("WEB.THEME", "$R::theme");
	$cfg->param("WEB.ICONSET", "$R::iconset");

	$cfg->save();
	
	# Template output
	&save;

	exit;

}

# Navbar
our %navbar;
$navbar{1}{Name} = "$L{'SETTINGS.LABEL_WU_SETTINGS'}";
$navbar{1}{URL} = 'index.cgi?form=1';

$navbar{2}{Name} = "$L{'SETTINGS.LABEL_MINISERVERCONNECTION'}";
$navbar{2}{URL} = 'index.cgi?form=2';

$navbar{3}{Name} = "$L{'SETTINGS.LABEL_CLOUDEMU'} / $L{'SETTINGS.LABEL_WEBSITE'}";
$navbar{3}{URL} = 'index.cgi?form=3';

$navbar{4}{Name} = "$L{'SETTINGS.LABEL_LOG'}";
$navbar{4}{URL} = "/admin/system/tools/logfile.cgi?logfile=plugins/$lbpplugindir/wu4lox.log&header=html&format=template&only=once";
$navbar{4}{target} = '_blank';

# Menu: Wunderground
if ($R::form eq "1" || !$R::form) {

  $navbar{1}{active} = 1;
  $template->param( "FORM1", 1);
  $template->param( FORMNO => '1' );

  my @values;
  my %labels;
  
  # Statiotyp
  @values = ('statid', 'coord', 'autoip');
  %labels = (
        'statid' => $L{'SETTINGS.LABEL_STATIONID'},
        'coord' => $L{'SETTINGS.LABEL_COORDINATES'},
        'autoip' => $L{'SETTINGS.LABEL_IPADDRESS'},
    );
  my $stationtyp = $cgi->radio_group(
        -name    => 'stationtyp',
        -id      => 'stationtyp',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.STATIONTYP'),
	-onClick => "disable()",
    );
  $template->param( STATIONTYP => $stationtyp );

  # WU Language
  @values = ('CZ', 'DL', 'EN', 'SP', 'FR' );
  %labels = (
        'DL' => 'Deutsch',
        'EN' => 'English',
        'FR' => 'Francaise',
        'SP' => 'Español',
        'CZ' => 'Český',
    );
  my $wulang = $cgi->popup_menu(
        -name    => 'wulang',
        -id      => 'wulang',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.WULANG'),
    );
  $template->param( WULANG => $wulang );

  # Units
  @values = ('1', '0' );
  %labels = (
        '1' => $L{'SETTINGS.LABEL_METRIC'},
        '0' => $L{'SETTINGS.LABEL_IMPERIAL'},
    );
  my $metric = $cgi->popup_menu(
        -name    => 'metric',
        -id      => 'metric',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.METRIC'),
    );
  $template->param( METRIC => $metric );

  # GetWUData
  @values = ('0', '1' );
  %labels = (
        '0' => $L{'SETTINGS.LABEL_OFF'},
        '1' => $L{'SETTINGS.LABEL_ON'},
    );
  my $getwudata = $cgi->popup_menu(
        -name    => 'getwudata',
        -id      => 'getwudata',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.GETWUDATA'),
    );
  $template->param( GETWUDATA => $getwudata );

  # Cron
  @values = ('1', '3', '5', '10', '15', '30', '60' );
  %labels = (
        '1' => $L{'SETTINGS.LABEL_1MINUTE'},
        '3' => $L{'SETTINGS.LABEL_3MINUTE'},
        '5' => $L{'SETTINGS.LABEL_5MINUTE'},
        '10' => $L{'SETTINGS.LABEL_10MINUTE'},
        '15' => $L{'SETTINGS.LABEL_15MINUTE'},
        '30' => $L{'SETTINGS.LABEL_30MINUTE'},
        '60' => $L{'SETTINGS.LABEL_60MINUTE'},
    );
  my $cron = $cgi->popup_menu(
        -name    => 'cron',
        -id      => 'cron',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.CRON'),
    );
  $template->param( CRON => $cron );

# Menu: Miniserver
} elsif ($R::form eq "2") {
  $navbar{2}{active} = 1;
  $template->param( "FORM2", 1);

  # SendUDP
  @values = ('0', '1' );
  %labels = (
        '0' => $L{'SETTINGS.LABEL_OFF'},
        '1' => $L{'SETTINGS.LABEL_ON'},
    );
  my $sendudp = $cgi->popup_menu(
        -name    => 'sendudp',
        -id      => 'sendudp',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.SENDUDP'),
    );
  $template->param( SENDUDP => $sendudp );

  # DFC
  my $dfc;
  my $n;
  my $checked;
  my @fields = split(/;/,$cfg->param('SERVER.SENDDFC'));
  for (my $i=1;$i<=4;$i++) {
    $checked = 0;
    foreach ( split( /;/,$cfg->param('SERVER.SENDDFC') ) ) {
      if ($_ eq $i) {
        $checked = 1;
      }
    }
    $n = $i-1;
    $dfc .= $cgi->checkbox(
        -name    => "dfc$i",
        -id      => "dfc$i",
	-checked => $checked,
        -value   => '1',
	-label   => "+$n $L{'SETTINGS.LABEL_DAYS'}",
      );
  }
  $template->param( DFC => $dfc );

  # HFC
  my $hfc;
  @fields = split(/;/,$cfg->param('SERVER.SENDHFC'));
  for ($i=1;$i<=36;$i++) {
    $checked = 0;
    foreach ( split( /;/,$cfg->param('SERVER.SENDHFC') ) ) {
      if ($_ eq $i) {
        $checked = 1;
      }
    }
    $hfc .= $cgi->checkbox(
        -name    => "hfc$i",
        -id      => "hfc$i",
	-checked => $checked,
        -value   => '1',
	-label   => "+$i $L{'SETTINGS.LABEL_HOURS'}",
      );
  }
  $template->param( HFC => $hfc );

# Menu: Cloudweather / Website
} elsif ($R::form eq "3") {
  $navbar{3}{active} = 1;
  $template->param( "FORM3", 1);
  
  # Check for installed DNSMASQ-Plugin
  my $checkdnsmasq = `cat $lbhomedir/data/system/plugindatabase.dat | grep -c -i DNSmasq`;
  if ($checkdnsmasq > 0) {
    $template->param( EMUWARNING => $L{'ERR_DNSMASQ_PLUGIN'} );
  }

  # Cloudweather Emu
  @values = ('0', '1' );
  %labels = (
        '0' => $L{'SETTINGS.LABEL_OFF'},
        '1' => $L{'SETTINGS.LABEL_ON'},
    );
  my $emu = $cgi->popup_menu(
        -name    => 'emu',
        -id      => 'emu',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('SERVER.EMU'),
    );
  $template->param( EMU => $emu );

  # Theme
  @values = ('dark', 'light', 'custom' );
  %labels = (
        'dark' => "Dark Theme",
        'light' => "Light Theme",
        'custom' => "Custom Theme",
    );
  my $theme = $cgi->popup_menu(
        -name    => 'theme',
        -id      => 'theme',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('WEB.THEME'),
    );
  $template->param( THEME => $theme );

  # Icon Set
  @values = ('color', 'flat', 'dark', 'light', 'green', 'silver', 'realistic', 'custom' );
  %labels = (
        'color' => "Color Set",
        'flat' => "Flat Set",
        'dark' => "Dark Set",
        'light' => "Light Set",
        'green' => "Green Set",
        'silver' => "Silver Set",
        'realistic' => "Realistic Set",
        'custom' => "Custom Set",
    );
  my $iconset = $cgi->popup_menu(
        -name    => 'iconset',
        -id      => 'iconset',
        -values  => \@values,
	-labels  => \%labels,
	-default => $cfg->param('WEB.ICONSET'),
    );
  $template->param( ICONSET => $iconset );

}

# Template Vars and Form parts
$template->param( "LBPPLUGINDIR", $lbpplugindir);

# Template
LoxBerry::Web::lbheader($L{'SETTINGS.LABEL_PLUGINTITLE'} . " V$version", "http://www.loxwiki.eu/display/LOXBERRY/Any+Plugin", "help.html");
print $template->output();
LoxBerry::Web::lbfooter();

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
        my $query = "$wuurl\/$R::apikey\/conditions\/pws:1\/lang:EN\/q\/$querystation\.json";

        my $ua = new LWP::UserAgent;
        my $res = $ua->get($query);
        my $json = $res->decoded_content();

        # Check status of request
        my $urlstatus = $res->status_line;
        my $urlstatuscode = substr($urlstatus,0,3);

	if ($urlstatuscode ne "200") {
                $error = $L{'SETTINGS.ERR_NO_DATA'} . "<br><br><b>URL:</b> $query<br><b>STATUS CODE:</b> $urlstatuscode";
                &error;
	}

        # Decode JSON response from server
        our $decoded_json = decode_json( $json );

	return();

}

#####################################################
# Error
#####################################################

sub error
{
	$template->param( "ERROR", 1);
	$template->param( "ERRORMESSAGE", $error);
	LoxBerry::Web::lbheader($L{'SETTINGS.LABEL_PLUGINTITLE'} . " V$version", "http://www.loxwiki.eu/display/LOXBERRY/Any+Plugin", "help.html");
	print $template->output();
	LoxBerry::Web::lbfooter();

	exit;
}

#####################################################
# Error
#####################################################

sub save
{
	$template->param( "SAVE", 1);
	LoxBerry::Web::lbheader($L{'SETTINGS.LABEL_PLUGINTITLE'} . " V$version", "http://www.loxwiki.eu/display/LOXBERRY/Any+Plugin", "help.html");
	print $template->output();
	LoxBerry::Web::lbfooter();

	exit;
}

