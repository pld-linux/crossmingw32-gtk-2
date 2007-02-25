Summary:	The Gimp Toolkit - Ming32 cross version
Summary(cs.UTF-8):	Sada nástrojů pro Gimp
Summary(de.UTF-8):	Der Gimp-Toolkit
Summary(es.UTF-8):	Conjunto de herramientas Gimp
Summary(fi.UTF-8):	Gimp-työkalukokoelma
Summary(fr.UTF-8):	Le toolkit de Gimp
Summary(it.UTF-8):	Il toolkit per Gimp
Summary(pl.UTF-8):	Gimp Toolkit - wersja skrośna dla Ming32
Summary(pt_BR.UTF-8):	Kit de ferramentas Gimp
Summary(tr.UTF-8):	Gimp ToolKit arayüz kitaplığı
%define		_realname   gtk+2
Name:		crossmingw32-%{_realname}
Version:	2.10.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/gtk+/2.10/gtk+-%{version}.tar.bz2
# Source0-md5:	20d763198efb38263b22dee347f69da6
Patch0:		%{name}-static.patch
Patch1:		%{name}-build.patch
URL:		http://www.gtk.org/
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-libtiff
BuildRequires:	unzip
Requires:	crossmingw32-glib2 >= 2.4.7
Requires:	crossmingw32-atk >= 1.6.0
Requires:	crossmingw32-pango >= 1.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abivers	2.10.0

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
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

%description -l cs.UTF-8
Knihovny X původně psané pro GIMP, které nyní používá také řada jiných
programů.

%description -l da.UTF-8
X biblioteker, oprindeligt udviklet til GIMP, men anvendes nu af flere
forskellige programmer.

%description -l de.UTF-8
Die X-Libraries, die ursprünglich für GIMP geschrieben wurden und
mittlerweile für eine ganze Reihe anderer Programme benutzt werden.

%description -l fr.UTF-8
X-kirjastot, jotka alunperin kirjoitettiin GIMP:lle, mutta joita
käytetään nyt myös useissa muissakin ohjelmissa.

%description -l it.UTF-8
Libreria X scritta per GIMP. Viene usata da diversi programmi.

%description -l pl.UTF-8
GTK+, która to biblioteka stała się podstawą programu Gimp, zawiera
funkcje do tworzenia graficznego interfejsu użytkownika pod X Window.
Była tworzona z założeniem żeby była mała, efektywna i wygodna. GTK+
jest napisane w C z podejściem zorientowanym bardzo obiektowo. GDK
(część GTK+) jest warstwą pośrednią pomiędzy Xlib i resztą toolkitu
zapewniającą pracę niezależnie od głębi koloru (ilości bitów na
piksel). GTK (druga część GTK+) jest natomiast już zbiorem różnego
rodzaju kontrolek służących do tworzenia interfejsu użytkownika.

%description -l pt_BR.UTF-8
Bibliotecas X originalmente escritas para o GIMP, que agora estão
sendo também usadas por vários outros programas.

%description -l tr.UTF-8
Başlangıçta GIMP için yazılmış X kitaplıkları. Şu anda başka
programlarca da kullanılmaktadır.

%prep
%setup -q -n gtk+-%{version}
#%patch0 -p1
#%patch1 -p1

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
	--without-xinput \
	--enable-static

#%{__sed} -i -e 's/^deplibs_check_method=.*/deplibs_check_method="pass_all"/' libtool

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0 \
	$RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{abivers}/filesystems

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir} \
	pkgconfigdir=%{_pkgconfigdir}

touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gtk.immodules

# remove unsupported locale scheme
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/en@IPA
# shut up check-files (static modules and *.la for modules)
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-*/2.*/*/*.{a,la}

# for various GTK+2 modules
#install -d $(echo $RPM_BUILD_ROOT%{_libdir}/gtk-*)/modules

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/{az_IR,uz@Latn}

%find_lang %{name} --all-name
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_includedir}/gtk-2.0
%{_libdir}/*.dll.a
%dir %{_libdir}/gtk-2.0
%{_libdir}/gtk-2.0/*
%{_pkgconfigdir}/*.pc
# XXX: missing dir
%dir %{_datadir}/gtk-2.0
%{_datadir}/gtk-2.0/*
