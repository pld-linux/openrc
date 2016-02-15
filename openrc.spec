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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenRC is a dependency-based init system that works with the
system-provided init program, normally /sbin/init. Currently, it does
not have an init program of its own.

%package start-stop-daemon
Summary:	start-stop-daemon - ensures that daemons start and stop
Group:		Applications/System

%description start-stop-daemon
start-stop-daemon provides a consistent method of starting, stopping
and signaling daemons.

%prep
%setup -q

cat <<EOF >> Makefile.inc
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
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{without openrc}
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}
%{__rm} -r $RPM_BUILD_ROOT/lib
%{__rm} -r $RPM_BUILD_ROOT/libexec
%{__rm} -r $RPM_BUILD_ROOT/sbin
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/lib
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/libexec
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/rc-status
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

%files start-stop-daemon
%defattr(644,root,root,755)
%{_mandir}/man8/start-stop-daemon.8*
%attr(755,root,root) %{_sbindir}/start-stop-daemon
