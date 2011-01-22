%define	name	ratpoison
%define version 1.4.5
%define release %mkrel 2

Name:		%{name}
Summary:	Simple Window Manager largely modelled after Screen
Group:		Graphical desktop/Other
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://www.nongnu.org/ratpoison/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:	http://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz
Patch0:		ratpoison-1.4.5-link.patch
BuildRequires:	libx11-devel
BuildRequires:	libxft-devel
BuildRequires:	libxtst-devel
BuildRequires:	libxinerama-devel
BuildRequires:	readline-devel

%description
Ratpoison is a simple window manager with no large library dependencies,
no fancy graphics, no window decorations, and no rodent dependence. It
is largely modeled after GNU Screen, which has done wonders in the
virtual terminal market. All interaction with the window manager is done
through keystrokes. ratpoison has a prefix map to minimize the key
clobbering that cripples EMACS and other quality pieces of software. All
windows are maximized and kept maximized to avoid wasting precious
screen space.

%prep
%setup -q
%patch0 -p0

%build
export CFLAGS="%optflags -DHAVE_GETLINE"
autoreconf -fi
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -rf %{buildroot}/usr/share/doc/%{name}

# startfile
%{__cat} > $RPM_BUILD_ROOT%{_bindir}/start%{name} << EOF
exec %{_bindir}/%{name}
EOF

# session file
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d
%{__cat} > $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d/16%{name} << EOF
NAME=%{name}
EXEC=%{_bindir}/start%{name}
DESC=%{name} window manager
SCRIPT:
exec %{_bindir}/start%{name}
EOF


%clean
rm -rf ${RPM_BUILD_ROOT}

%post
%_install_info %{name}.info

%postun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc INSTALL README TODO doc/ipaq.ratpoisonrc doc/sample.ratpoisonrc AUTHORS COPYING contrib/genrpbindings contrib/split.sh NEWS
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/16%{name}
%attr(644,root,root) %{_mandir}/man1/%{name}.1*
%attr(644,root,root) %{_infodir}/%{name}.info*
%{_datadir}/%{name}
%defattr(755,root,root,755)
%{_bindir}/start%{name}
%{_bindir}/%{name}
%{_bindir}/rpws


