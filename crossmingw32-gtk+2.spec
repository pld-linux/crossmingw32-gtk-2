Summary:	The Gimp Toolkit - Ming32 cross version
Summary(pl.UTF-8):	Gimp Toolkit - wersja skrośna dla Ming32
%define		_realname   gtk+2
Name:		crossmingw32-%{_realname}
Version:	2.10.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/gtk+/2.10/gtk+-%{version}.tar.bz2
# Source0-md5:	20d763198efb38263b22dee347f69da6
Patch0:		%{name}-w32api.patch
URL:		http://www.gtk.org/
BuildRequires:	crossmingw32-atk >= 1.6.0
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-glib2 >= 2.4.7
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-libtiff
BuildRequires:	crossmingw32-pango >= 1.4.1
Requires:	crossmingw32-atk >= 1.6.0
Requires:	crossmingw32-glib2 >= 2.4.7
Requires:	crossmingw32-pango >= 1.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abivers	2.10.0

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%define         filterout_ld            (-Wl,)?-as-needed.*

%description
GTK+, which stands for the Gimp ToolKit, is a library for creating
graphical user interfaces for the X Window System. It is designed to
be small, efficient, and flexible. GTK+ is written in C with a very
object-oriented approach. GDK (part of GTK+) is a drawing toolkit
which provides a thin layer over Xlib to help automate things like
dealing with different color depths, and GTK is a widget set for
creating user interfaces.

This package contains the cross version for Win32.

%description -l pl.UTF-8
GTK+, która to biblioteka stała się podstawą programu Gimp, zawiera
funkcje do tworzenia graficznego interfejsu użytkownika pod X Window.
Była tworzona z założeniem żeby była mała, efektywna i wygodna. GTK+
jest napisane w C z podejściem zorientowanym bardzo obiektowo. GDK
(część GTK+) jest warstwą pośrednią pomiędzy Xlib i resztą toolkitu
zapewniającą pracę niezależnie od głębi koloru (ilości bitów na
piksel). GTK (druga część GTK+) jest natomiast już zbiorem różnego
rodzaju kontrolek służących do tworzenia interfejsu użytkownika.

Ten pakiet zawiera wersję skrośną dla Win32.

%package dll
Summary:	DLL GTK+ libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL GTK+ dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-atk-dll >= 1.6.0
Requires:	crossmingw32-glib2-dll >= 2.4.7
Requires:	crossmingw32-pango-dll >= 1.4.1
Requires:	wine

%description dll
DLL GTK+ libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL GTK+ dla Windows.

%prep
%setup -q -n gtk+-%{version}
%patch0 -p1

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-gtk-doc \
	--disable-man \
	--disable-modules \
	--disable-xkb \
	--with-gdk-target=win32 \
	--without-x \
	--without-xinput

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# remove unsupported locale scheme
rm -rf $RPM_BUILD_ROOT%{_datadir}/{aclocal,gtk-2.0,gtk-doc,locale,man,themes}
# shut up check-files (static modules and *.la for modules)
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-*/2.*/*/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libg[dt]k*.dll.a
%{_libdir}/libg[dt]k*.la
%{_libdir}/g[dt]k*.def
%dir %{_libdir}/gtk-2.0
%{_libdir}/gtk-2.0/include
%{_includedir}/gtk-2.0
%{_includedir}/gtk-unix-print-2.0
%{_pkgconfigdir}/*.pc

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libg[dt]k*.dll
