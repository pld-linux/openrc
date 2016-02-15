#
# Conditional build:
%bcond_with	openrc		# package OpenRC files

Summary:	OpenRC manages the services, startup and shutdown of a host
Name:		openrc
Version:	0.20.4
Release:	0.1
License:	BSD
Group:		Base
Source0:	https://github.com/OpenRC/openrc/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	12e1e2c70c03f93fb42f3549d8cdbc0a
URL:		https://github.com/OpenRC/openrc
BuildRequires:	libselinux-devel
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenRC is a dependency-based init system that works with the
system-provided init program, normally /sbin/init. Currently, it does
not have an init program of its own.

%package libs
Summary:	OpenRC libraries
Group:		Libraries

%description libs
OpenRC libraries

%package start-stop-daemon
Summary:	start-stop-daemon - ensures that daemons start and stop
Group:		Applications/System
Requires:	%{name}-libs = %{version}-%{release}

%description start-stop-daemon
start-stop-daemon provides a consistent method of starting, stopping
and signaling daemons.

start-stop-daemon first appeared in Debian.

This is a complete re-implementation with the process finding code in
the OpenRC library (librc, -lrc) so other programs can make use of it.

%prep
%setup -q

cat <<EOF >> Makefile.inc
LIBNAME=%{_lib}
MKNET=no
MKPAM=pam
MKPREFIX=yes
MKPKGCONFIG=no
MKSELINUX=yes
MKSTATICLIBS=no
MKTERMCAP=ncurses
MKTOOLS=yes
PKG_PREFIX=%{_prefix}/pkg
LOCAL_PREFIX=%{_prefix}/local
PREFIX=%{_prefix}
BRANDING="PLD-Linux/$(uname -s)"
EOF

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT{%{_sbindir},/sbin}/start-stop-daemon

%if %{without openrc}
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}
%{__rm} -r $RPM_BUILD_ROOT/libexec
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/lib
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/libexec
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/rc-status
%{__rm} -r $RPM_BUILD_ROOT%{_sbindir}
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man3
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man8/openrc*
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man8/rc*
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man8/service*
%{__rm} $RPM_BUILD_ROOT/sbin/rc-sstat
%{__rm} $RPM_BUILD_ROOT/lib/*.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with openrc}
%files
%defattr(644,root,root,755)
%doc AUTHORS TODO ChangeLog LICENSE *.md
%attr(755,root,root) %{_sbindir}/openrc
%attr(755,root,root) %{_sbindir}/openrc-run
%attr(755,root,root) %{_sbindir}/rc
%attr(755,root,root) %{_sbindir}/rc-service
%attr(755,root,root) %{_sbindir}/rc-update
%attr(755,root,root) %{_sbindir}/runscript
%attr(755,root,root) %{_sbindir}/service
%{_mandir}/man3/e*.3*
%{_mandir}/man3/rc*.3*
%{_mandir}/man8/openrc-run.8*
%{_mandir}/man8/openrc.8*
%{_mandir}/man8/rc-service.8*
%{_mandir}/man8/rc-sstat.8*
%{_mandir}/man8/rc-status.8*
%{_mandir}/man8/rc-update.8*
%{_mandir}/man8/service.8
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libeinfo.so.1
%attr(755,root,root) /lib/librc.so.1

%files start-stop-daemon
%defattr(644,root,root,755)
%{_mandir}/man8/start-stop-daemon.8*
%attr(755,root,root) /sbin/start-stop-daemon
