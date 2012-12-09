Summary:        Utility for removing files based on when they were last accessed
Name:           tmpwatch
Version:        2.10.1
Release:        %mkrel 3
Group:          File tools
License:	GPLv2
URL:		https://fedorahosted.org/tmpwatch/
Source0:        https://fedorahosted.org/releases/t/m/tmpwatch/%{name}-%{version}.tar.bz2
Requires:       psmisc
# configure is looking for /sbin/fuser
BuildRequires: psmisc
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The tmpwatch utility recursively searches through specified directories and
removes files which have not been accessed in a specified period of time.
Tmpwatch is normally used to clean up directories which are used for
temporarily holding files (for example, /tmp). Tmpwatch ignores symlinks,
won't switch filesystems and only removes empty directories and regular files.

%prep

%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall ROOT=%{buildroot} MANDIR=%{_mandir} SBINDIR=%{_sbindir}

install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/sysconfig

cat > tmpwatch.cron << EOF
#!/bin/sh

[ -f %{_sysconfdir}/sysconfig/tmpwatch ] && . %{_sysconfdir}/sysconfig/tmpwatch

%{_sbindir}/tmpwatch \$TMPWATCH_OPTIONS \$TMPWATCH_EXCLUDES 10d /tmp

%{_sbindir}/tmpwatch \$TMPWATCH_OPTIONS \$TMPWATCH_EXCLUDES 30d /var/tmp

[ -f %{_sysconfdir}/sysconfig/i18n ] && . %{_sysconfdir}/sysconfig/i18n

for d in /var/{cache/man,catman}/{cat?,X11R6/cat?,local/cat?,\$LANG/cat?}; do
    if [ -d "\$d" ]; then
        %{_sbindir}/tmpwatch \$TMPWATCH_OPTIONS -f 30d "\$d"
    fi
done
EOF

cat > tmpwatch.sysconfig << EOF
#TMPWATCH_OPTIONS="-umc"
# (oe) define files/directories/sockets tmpwatch should ignore (#18488)
TMPWATCH_EXCLUDES="-x /tmp/.ICE-unix -x /tmp/.X*-unix -x /tmp/.font-unix -x /tmp/.Test-unix"
EOF

install -m0755 tmpwatch.cron %{buildroot}%{_sysconfdir}/cron.daily/tmpwatch
install -m0644 tmpwatch.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/tmpwatch

cat > README.urpmi << EOF
The %{_sysconfdir}/cron.daily/tmpwatch script has been changed to use the %{_sysconfdir}/sysconfig/tmpwatch 
file to exclude certain files/directories/sockets from being processed. It should be safe to make your changes
there instead. Per default these are not touched by tmpwatch:

/tmp/.ICE-unix /tmp/.X*-unix /tmp/.font-unix /tmp/.Test-unix
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.urpmi ChangeLog NEWS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/tmpwatch
%attr(0755,root,root) %{_sysconfdir}/cron.daily/tmpwatch
%{_sbindir}/tmpwatch
%{_mandir}/man8/tmpwatch.8*


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.10.1-2mdv2011.0
+ Revision: 670712
- mass rebuild

* Sun Aug 15 2010 Emmanuel Andry <eandry@mandriva.org> 2.10.1-1mdv2011.0
+ Revision: 570137
- ?\194New version 2.10.1

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 2.9.17-1mdv2010.1
+ Revision: 484032
- update to new version 2.9.17

* Tue Aug 11 2009 Emmanuel Andry <eandry@mandriva.org> 2.9.15-1mdv2010.0
+ Revision: 415139
- New version 2.9.15
- add source url

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.13-4mdv2009.1
+ Revision: 317901
- use %%ldflags

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 2.9.13-3mdv2009.0
+ Revision: 265766
- rebuild early 2009.0 package (before pixel changes)

* Mon May 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.13-2mdv2009.0
+ Revision: 201367
- revert the last change for now.
- make the cron script take arguments

* Mon Apr 21 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.13-1mdv2009.0
+ Revision: 196204
- 2.9.13
- exclude some more files/directories/sockets from pruning

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Nov 10 2007 David Walluck <walluck@mandriva.org> 2.9.11-1mdv2008.1
+ Revision: 107391
- 2.9.11

* Wed Aug 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9.10-2mdv2008.0
+ Revision: 60382
- added /tmp/jack-* directories to be excluded from pruning


* Sun Dec 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9.10-1mdv2007.0
+ Revision: 102995
- 2.9.10
- fix #22298
- Import tmpwatch

* Fri Jun 30 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.9.7-1mdv2007.0
- 2.9.7
- fix executable-marked-as-config-file
- fix macro-in-%%changelog
- fix mixed-use-of-spaces-and-tabs

* Sat Dec 31 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.9.6-1mdk
- 2.9.6
- happy new year!:)

* Sat Nov 05 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9.4-2mdk
- added the %%{_sysconfdir}/sysconfig/tmpwatch file in an attempt to 
  fix #18488 (tmpwatch breaks graphical login after 10 days uptime)

* Sun Jul 10 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.9.4-1mdk
- 2.9.4
- %%mkrel

* Mon Jan 10 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.9.2-1mdk
- 2.9.2
- wipe out buildroot at the beginning of %%install
- fix summary-ended-with-dot

* Fri Nov 12 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.9.1-1mdk
- 2.9.1
- cosmetics

