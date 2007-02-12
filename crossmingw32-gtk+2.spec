Summary:	The Gimp Toolkit - Ming32 cross version
Summary(cs.UTF-8):   Sada nástrojů pro Gimp
Summary(de.UTF-8):   Der Gimp-Toolkit
Summary(es.UTF-8):   Conjunto de herramientas Gimp
Summary(fi.UTF-8):   Gimp-työkalukokoelma
Summary(fr.UTF-8):   Le toolkit de Gimp
Summary(it.UTF-8):   Il toolkit per Gimp
Summary(pl.UTF-8):   Gimp Toolkit - wersja skrośna dla Ming32
Summary(pt_BR.UTF-8):   Kit de ferramentas Gimp
Summary(tr.UTF-8):   Gimp ToolKit arayüz kitaplığı
Name:		crossmingw32-gtk+2
Version:	2.4.13
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.gimp.org/~tml/gimp/win32/gtk+-dev-%{version}.zip
# Source0-md5:	36542202e50d8f3a9551072ae72188bf
URL:		http://www.gtk.org/
BuildRequires:	unzip
Requires:	crossmingw32-glib2 >= 2.4.7
Requires:	crossmingw32-atk >= 1.6.0
Requires:	crossmingw32-pango >= 1.4.1
Requires:	crossmingw32-pango < 1.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

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
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/share

# omit man,share/aclocal,share/gtk-doc (they are system-wide)
cp -rf bin include lib $RPM_BUILD_ROOT%{arch}
cp -rf share/gtk-2.0 $RPM_BUILD_ROOT%{arch}/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/gtk-2.0
%{arch}/lib/*.lib
%{arch}/lib/*.dll.a
%{arch}/lib/gtk-2.0
%{arch}/lib/pkgconfig/*.pc
# XXX: missing dir
%{arch}/share/gtk-2.0
