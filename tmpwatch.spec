Summary:        Utility for removing files based on when they were last accessed
Name:           tmpwatch
Version:        2.9.13
Release:        %mkrel 1
Group:          File tools
License:	GPLv2
URL:		https://fedorahosted.org/tmpwatch/
Source0:        %{name}-%{version}.tar.bz2
Requires:       psmisc
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
%make RPM_OPT_FLAGS="%{optflags}"

%install
rm -rf %{buildroot}

%makeinstall ROOT=%{buildroot} MANDIR=%{_mandir} SBINDIR=%{_sbindir}

install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/sysconfig

cat > tmpwatch.cron << EOF
#!/bin/sh

[ -f %{_sysconfdir}/sysconfig/tmpwatch ] && . %{_sysconfdir}/sysconfig/tmpwatch

%{_sbindir}/tmpwatch \$TMPWATCH_EXCLUDES 10d /tmp

%{_sbindir}/tmpwatch \$TMPWATCH_EXCLUDES 30d /var/tmp

[ -f %{_sysconfdir}/sysconfig/i18n ] && . %{_sysconfdir}/sysconfig/i18n

for d in /var/{cache/man,catman}/{cat?,X11R6/cat?,local/cat?,\$LANG/cat?}; do
    if [ -d "\$d" ]; then
        %{_sbindir}/tmpwatch -f 30d "\$d"
    fi
done
EOF

cat > tmpwatch.sysconfig << EOF
# (oe) define files/directories/sockets tmpwatch should ignore (#18488)
TMPWATCH_EXCLUDES="-x /tmp/.ICE-unix -x /tmp/.X*-unix -x /tmp/.font-unix -x /tmp/.Test-unix -x /tmp/jack-* -x /tmp/.esd-* -x /tmp/pulse-* -x /tmp/acroread* -x /tmp/gconfd-*"
EOF

install -m0755 tmpwatch.cron %{buildroot}%{_sysconfdir}/cron.daily/tmpwatch
install -m0644 tmpwatch.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/tmpwatch

cat > README.urpmi << EOF
The %{_sysconfdir}/cron.daily/tmpwatch script has been changed to use the %{_sysconfdir}/sysconfig/tmpwatch 
file to exclude certain files/directories/sockets from being processed. It should be safe to make your changes
there instead. Per default these are not touched by tmpwatch:

/tmp/.ICE-unix /tmp/.X*-unix /tmp/.font-unix /tmp/.Test-unix /tmp/jack-* /tmp/.esd-* /tmp/pulse-* /tmp/acroread* /tmp/gconfd-*
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
