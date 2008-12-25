Summary:	The GIMP Toolkit - Ming32 cross version
Summary(pl.UTF-8):	GIMP Toolkit - wersja skrośna dla Ming32
Name:		crossmingw32-gtk+2
Version:	2.14.6
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtk+/2.14/gtk+-%{version}.tar.bz2
# Source0-md5:	69c2d2842203d7b627bc6ec34cb4a4f8
URL:		http://www.gtk.org/
BuildRequires:	crossmingw32-atk >= 1.24.0
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-glib2 >= 2.18.0
BuildRequires:	crossmingw32-jasper
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-pango >= 1.22.0
BuildRequires:	pkgconfig >= 1:0.15
Requires:	crossmingw32-atk >= 1.24.0
Requires:	crossmingw32-glib2 >= 2.18.0
Requires:	crossmingw32-pango >= 1.22.0
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

#define         filterout_ld            (-Wl,)?-as-needed.*

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

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
Requires:	crossmingw32-atk-dll >= 1.24.0
Requires:	crossmingw32-glib2-dll >= 2.18.0
Requires:	crossmingw32-pango-dll >= 1.22.0
Requires:	wine

%description dll
DLL GTK+ libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL GTK+ dla Windows.

%prep
%setup -q -n gtk+-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	ac_cv_path_CUPS_CONFIG=no \
	--target=%{target} \
	--host=%{target} \
	--disable-gtk-doc \
	--disable-man \
	--disable-xkb \
	--with-gdktarget=win32 \
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
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.{a,la}
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.*/*/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libgailutil.dll.a
%{_libdir}/libgdk-win32-2.0.dll.a
%{_libdir}/libgdk_pixbuf-2.0.dll.a
%{_libdir}/libgtk-win32-2.0.dll.a
%{_libdir}/libgailutil.la
%{_libdir}/libgdk-win32-2.0.la
%{_libdir}/libgdk_pixbuf-2.0.la
%{_libdir}/libgtk-win32-2.0.la
%{_libdir}/gdk-win32-2.0.def
%{_libdir}/gdk_pixbuf-2.0.def
%{_libdir}/gtk-win32-2.0.def
%dir %{_libdir}/gtk-2.0
%{_libdir}/gtk-2.0/include
%{_includedir}/gail-1.0
%{_includedir}/gtk-2.0
%{_includedir}/gtk-unix-print-2.0
%{_pkgconfigdir}/gail.pc
%{_pkgconfigdir}/gdk-2.0.pc
%{_pkgconfigdir}/gdk-pixbuf-2.0.pc
%{_pkgconfigdir}/gdk-win32-2.0.pc
%{_pkgconfigdir}/gtk+-2.0.pc
%{_pkgconfigdir}/gtk+-win32-2.0.pc

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libgailutil-*.dll
%{_dlldir}/libgdk-win32-2.0-*.dll
%{_dlldir}/libgdk_pixbuf-2.0-*.dll
%{_dlldir}/libgtk-win32-2.0-*.dll
