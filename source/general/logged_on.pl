#!/usr/bin/perl

# The "Am I logged in?" story script > HTML file.
# This uses various information to determine if I am logged in or not, and
# where and when I was or was not logged in. This is a very early attempt of
# mine at Perl, so don't be too surprised if it's complete crap!

# This program outputs a HTML format file in ASCII.

# (c) Michael James Jan 1996.

# -------------------------------------------------------------------------

# First some constants for HTML.
$strong="<STRONG>";
$strong_="</STRONG>";
$em="<EM>";
$em_="</EM>";
$para="\n<P>\n";
$h1="<H1>";
$h1_="</H1>";
$center="<CENTER>";
$center_="</CENTER>\n";

# Now reset a couple of flags....
$i_am_logged_on=0;
$i_am_in_glasgow=0;

# Get the local time and date.
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

# Get the names of the days ready....
@day_names=('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday');

# ... and the names of the months.

@month_names=('January','February','March','April','May','June','July','August','September','October','November','December');

# Work out endings to numbers for dates (eg 1st, 2nd, 3rd, etc.)

for (1,21,31)      { $end_date[$_]="st" }
for (2,22)         { $end_date[$_]="nd" }
for (3,23)         { $end_date[$_]="rd" }
for (4..20,24..30) { $end_date[$_]="th" }

# If the figure for the number of minutes is in single figures, then make it
# into double figures.

for (0..9) 
{  if ($min==$_)      # If $min is in the range 0..9
   { $min="0".$min }  # ... Add extra zero figure to start of it.
}

# Work out 12 hour time from 24 hour hours

for (0..11)  { $time_12hr[$_]="$_:$min am" }
for (12..23) { $time_12hr[$_]=($_-12).":$min pm" }

$this_time="$time_12hr[$hour] and $sec seconds (local time) on $day_names[$wday] $mday$end_date[$mday] $month_names[$mon] 19$year";

# The following line tells the WWW server that an ASCII HTML is being output.
print"Content-type: text/html\n\n";

# Now that start of the HTML page proper.
print <<HEADER;
<HTML>
<HEAD>
<TITLE>Am I logged in?</TITLE>
</HEAD>
<BODY bgcolor=#ffffff>
<CENTER>
<H3 ALIGN=CENTER>Am I logged in?</H3>
HEADER

open(LASTUSER,".lastme");
  $last_time=<LASTUSER>;
close LASTUSER;

open(WHO, "w -hs |");
while (<WHO>) {
   if (/mjames/i)
   { $i_am_logged_on=1;
     if ($i_am_in_glasgow==0)
     { print $h1,"Yes!",$h1_,$para,$strong,"I am logged in from "; }
     elsif ($i_am_in_glasgow==1)
     { print"\n\nI am also logged in from "; }
      if (/lenzie/i)
      {print "my UNIX account at ";
       $i_am_in_glasgow=1;}
      elsif (/cent/i)
      {print "the Computing Services drop-in lab at ";
       $i_am_in_glasgow=1;
         if (/bo/i)
         {print"the Boyd Orr building, ";}
         else
         {print"the James Watt building, ";}
      }
      if ($i_am_in_glasgow==1)
      {print"Glasgow University."}
      else
      {print"an outside server!"}
   }
}
close(WHO);
if ($i_am_logged_on==0)
   {  print $h1,"Sorry!",$h1_,"\n";
      print"It appears I am not logged on....<br>\n\n";
		open (LAST, "last -1 mjames|");     # Open a pipe to last time I was on.
		$_=<LAST>;							      # Read a line (ie last time I was on).
		close LAST;                         # Close pipe.

      # Now to get the all important info from the line of text. The format is:
      # User nam        (Don't need, search past it - \s+)
      # Terminal        (Don't need, search past it - \S+\s+)
      # Last login from (Remember- (\S+)\s+ )
      # Day             (Remember- (\S+)\s+ )
      # Month           (Remember- (\S+)\s+ )
      # Month Day       (Remember- (\S+)\s+ )
      # Hour            (Remember- (\d+): )
      # Minutes         (Remember- (\d+) ) 
      ($last_domain, $last_day, $last_mon,$last_mday,$last_hour,$last_min)=/\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+):(\d+)/;
		print "I was last logged on at $last_day $last_mon $last_mday $last_hour:$last_min <br>\n";
	}
print $strong_,$center_,$para,"<HR>";
print $em,"(This page was updated on ",$this_time,")",$para,$para;
print "(Last updated on ",$last_time,")",$em_,"\n";
print <<ENDER;
<HR>
If you want to see the Perl script that did this, go 
<A HREF="http://grelb.src.gla.ac.uk:8000/~mjames/cgi-bin/me.pl">here</A>!
ENDER

open(LASTUSER,"> .lastme");
print LASTUSER $this_time;
close(LASTUSER);