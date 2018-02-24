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
use Config::Simple;
use File::HomeDir;
use Cwd 'abs_path';
use LWP::UserAgent;
use JSON qw( decode_json );
use utf8;
use Encode qw(encode_utf8);
#use warnings;
use strict;
no strict "refs"; # we need it for template system

##########################################################################
# Variables
##########################################################################

our $cfg;
our $pphrase;
our $lang;
our $template_title;
our $installdir;
our $planguagefile;
our $table;
our $version;
our $psubfolder;
my  $home = File::HomeDir->my_home;
our $search;
our $queryurl;
our $res;
our $ua;
our $json;
our $decoded_json;
our $urlstatus;
our $urlstatuscode;
our $i;
our $results;
our $decoded_json;
our $lat;
our $long;
our $numrestotal;

##########################################################################
# Read Settings
##########################################################################

# Version of this script
$version = "0.0.2";

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installdir      = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");

#########################################################################
# Parameter
#########################################################################

$search = param('search');
$search = quotemeta($search);

##########################################################################
# Language Settings
##########################################################################

# Standard is german
if ($lang eq "") {
  $lang = "de";
}

# If there's no template, use german
if (!-e "$installdir/templates/plugins/$psubfolder/$lang/language.dat") {
  $lang = "de";
}

# Read translations
$planguagefile = "$installdir/templates/plugins/$psubfolder/$lang/language.dat";
$pphrase = new Config::Simple($planguagefile);

##########################################################################
# Main program
##########################################################################

if ($search) {

  $queryurl = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=$search";

  # If we received a query, send it to Google API
  $ua = new LWP::UserAgent;
  $res = $ua->get($queryurl);

  $json=$res->decoded_content();
  $json = encode_utf8( $json );

  # JSON Answer
  $decoded_json = decode_json( $json );

  $urlstatus = $res->status_line;
  $urlstatuscode = substr($urlstatus,0,3);

  # Count results
  $numrestotal = 0;
  for my $results( @{$decoded_json->{results}} ){
    $numrestotal++;
  }
 
  if (!$numrestotal) {
    $table = "<tr><td align=\"center\">" . $pphrase->param("TXT0002") . "</td></tr>\n";
  } else { 
    $i = 1;
      for $results( @{$decoded_json->{results}} ){
        $lat = $results->{geometry}->{location}->{lat};
        $long = $results->{geometry}->{location}->{lng};
        $table = $table . "<tr><td align=\"right\">$i\.</td><td>$results->{formatted_address}</td>\n";
        $table = "$table" ."<td style=\"vertical-align: middle; text-align: center\"><button type=\"button\" data-role=\"button\" data-inline=\"true\" data-mini=\"true\" onClick=\"window.opener.document.getElementById('coordlat').value = '$lat';window.opener.document.getElementById('coordlong').value = '$long';window.close()\"> <font size=\"-1\">&Uuml;bernehmen</font></button></td></tr>\n";
        $i++;
      };
  }

}

print "Content-Type: text/html\n\n";

$template_title = $pphrase->param("TXT0000") . " - " . $pphrase->param("TXT0001");

# Print Template
open(F,"$installdir/templates/plugins/$psubfolder/$lang/addresslist.html") || die "Missing template /templates/plugins/$psubfolder/$lang/addresslist.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
