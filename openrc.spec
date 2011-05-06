Summary:	OpenRC manages the services, startup and shutdown of a host
Name:		openrc
Version:	0.6.1
Release:	0.1
License:	BSD
Group:		Base
Source0:	http://roy.marples.name/downloads/openrc/%{name}-%{version}.tar.bz2
# Source0-md5:	90aa095508b0e92b06eda43b641cba49
URL:		http://roy.marples.name/projects/openrc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenRC is a dependency based init system that works with the system
provided init program, normally /sbin/init. It is not a replacement
for /sbin/init. OpenRC is 100% compatible with Gentoo init scripts,
which means you can probably find one for the daemons you want to
start in the Gentoo Portage Tree. OpenRC also provides an init script
that runs BSD rc.d style scripts too, making it easy to port your BSD
system to OpenRC.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS CHANGES ChangeLog NEWS README THANKS TODO
