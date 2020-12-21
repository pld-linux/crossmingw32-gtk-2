Summary:	The GIMP Toolkit - MinGW32 cross version
Summary(pl.UTF-8):	GIMP Toolkit - wersja skrośna dla MinGW32
Name:		crossmingw32-gtk+2
Version:	2.24.33
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	https://download.gnome.org/sources/gtk+/2.24/gtk+-%{version}.tar.xz
# Source0-md5:	0118e98dbe0e4dab90ce475f9f0e6c0c
URL:		https://www.gtk.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.7
BuildRequires:	crossmingw32-atk >= 1.30.0
BuildRequires:	crossmingw32-cairo >= 1.6
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-gdk-pixbuf2 >= 2.22.0
BuildRequires:	crossmingw32-glib2 >= 2.28.0
BuildRequires:	crossmingw32-pango >= 1.28.0
# glib-genmarshal, glib-mkenums
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gtk-doc >= 1.17
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-atk >= 1.30.0
Requires:	crossmingw32-cairo >= 1.6
Requires:	crossmingw32-gdk-pixbuf2 >= 2.22.0
Requires:	crossmingw32-glib2 >= 2.28.0
Requires:	crossmingw32-pango >= 1.28.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abivers	2.10.0

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%define		_ssp_cflags		%{nil}
%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
GTK+, which stands for the GIMP ToolKit, is a library for creating
graphical user interfaces for the X Window System. It is designed to
be small, efficient, and flexible. GTK+ is written in C with a very
object-oriented approach. GDK (part of GTK+) is a drawing toolkit
which provides a thin layer over Xlib to help automate things like
dealing with different color depths, and GTK is a widget set for
creating user interfaces.

This package contains the cross version for Win32.

%description -l pl.UTF-8
GTK+, która to biblioteka stała się podstawą programu GIMP, zawiera
funkcje do tworzenia graficznego interfejsu użytkownika pod X Window.
Była tworzona z założeniem żeby była mała, efektywna i wygodna. GTK+
jest napisane w C z podejściem zorientowanym bardzo obiektowo. GDK
(część GTK+) jest warstwą pośrednią pomiędzy Xlib a właściwym GTK
zapewniającą pracę niezależnie od głębi koloru (ilości bitów na
piksel). GTK (druga część GTK+) jest natomiast już zbiorem różnego
rodzaju kontrolek służących do tworzenia interfejsu użytkownika.

Ten pakiet zawiera wersję skrośną dla Win32.

%package dll
Summary:	DLL GTK+ libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL GTK+ dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-atk-dll >= 1.30.0
Requires:	crossmingw32-cairo-dll >= 1.6
Requires:	crossmingw32-gdk-pixbuf2-dll >= 2.22.0
Requires:	crossmingw32-glib2-dll >= 2.28.0
Requires:	crossmingw32-pango-dll >= 1.28.0
Requires:	wine

%description dll
DLL GTK+ libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL GTK+ dla Windows.

%prep
%setup -q -n gtk+-%{version}

# avoid rebuilding builtin stock icons cache
# (requires native gtk-update-icon-cache >= 2.24.24 < 3.0)
touch gtk/stamp-icons gtk/gtkbuiltincache.h

# -Wl, makes recent libtools pass it as linker flag before any objects,
# which is incompatible with as-needed; use plain -luuid with pass_all
# hack below
%{__sed} -i -e 's@-Wl,-luuid@-luuid@' configure.ac

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-cups \
	--disable-gtk-doc \
	--disable-man \
	--disable-xkb \
	--with-gdktarget=win32 \
	--without-x \
	--without-xinput

# by default mingw32 libtool doesn't allow to embed static libraries
# in shared libraries (only import libraries are allowed); override this
# to allow static libuuid
%{__sed} -i -e 's/^\(deplibs_check_method\)=.*/\1="pass_all"/' libtool
# avoid -luuid in shared linking
%{__sed} -i -e 's/ -luuid//;$aLibs.private: -luuid' gdk*.pc

%{__make} \
	GLIB_GENMARSHAL=/usr/bin/glib-genmarshal \
	GLIB_MKENUMS=/usr/bin/glib-mkenums

%install
rm -rf $RPM_BUILD_ROOT

# .def installation is not parallel-compliant
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# runtime
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/im-multipress.conf
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{gtk-2.0,locale,themes}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/gtk*.exe
# development - use from native gtk+2 if necessary
%{__rm} $RPM_BUILD_ROOT%{_bindir}/gtk-builder-convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{aclocal,gtk-doc}
# shut up check-files (static modules and *.la for modules)
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.{a,la}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.*/*/*.{a,la}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libgailutil.dll.a
%{_libdir}/libgdk-win32-2.0.dll.a
%{_libdir}/libgtk-win32-2.0.dll.a
%{_libdir}/gailutil.def
%{_libdir}/gdk-win32-2.0.def
%{_libdir}/gtk-win32-2.0.def
%dir %{_libdir}/gtk-2.0
%{_libdir}/gtk-2.0/include
%{_includedir}/gail-1.0
%{_includedir}/gtk-2.0
%{_pkgconfigdir}/gail.pc
%{_pkgconfigdir}/gdk-2.0.pc
%{_pkgconfigdir}/gdk-win32-2.0.pc
%{_pkgconfigdir}/gtk+-2.0.pc
%{_pkgconfigdir}/gtk+-win32-2.0.pc

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libgailutil-*.dll
%{_dlldir}/libgdk-win32-2.0-*.dll
%{_dlldir}/libgtk-win32-2.0-*.dll
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/2.10.0
%dir %{_libdir}/gtk-2.0/2.10.0/engines
%{_libdir}/gtk-2.0/2.10.0/engines/libpixmap.dll
%{_libdir}/gtk-2.0/2.10.0/engines/libwimp.dll
%dir %{_libdir}/gtk-2.0/2.10.0/immodules
%{_libdir}/gtk-2.0/2.10.0/immodules/im-*.dll
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libgail.dll
