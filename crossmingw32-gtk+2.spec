Summary:	The Gimp Toolkit - Ming32 cross version
Summary(cs):	Sada nástrojù pro Gimp
Summary(de):	Der Gimp-Toolkit
Summary(es):	Conjunto de herramientas Gimp
Summary(fi):	Gimp-työkalukokoelma
Summary(fr):	Le toolkit de Gimp
Summary(it):	Il toolkit per Gimp
Summary(pl):	Gimp Toolkit - wersja skro¶na dla Ming32
Summary(pt_BR):	Kit de ferramentas Gimp
Summary(tr):	Gimp ToolKit arayüz kitaplýðý
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

%description -l cs
Knihovny X pùvodnì psané pro GIMP, které nyní pou¾ívá také øada jiných
programù.

%description -l da
X biblioteker, oprindeligt udviklet til GIMP, men anvendes nu af flere
forskellige programmer.

%description -l de
Die X-Libraries, die ursprünglich für GIMP geschrieben wurden und
mittlerweile für eine ganze Reihe anderer Programme benutzt werden.

%description -l fr
X-kirjastot, jotka alunperin kirjoitettiin GIMP:lle, mutta joita
käytetään nyt myös useissa muissakin ohjelmissa.

%description -l it
Libreria X scritta per GIMP. Viene usata da diversi programmi.

%description -l pl
GTK+, która to biblioteka sta³a siê podstaw± programu Gimp, zawiera
funkcje do tworzenia graficznego interfejsu u¿ytkownika pod X Window.
By³a tworzona z za³o¿eniem ¿eby by³a ma³a, efektywna i wygodna. GTK+
jest napisane w C z podej¶ciem zorientowanym bardzo obiektowo. GDK
(czê¶æ GTK+) jest warstw± po¶redni± pomiêdzy Xlib i reszt± toolkitu
zapewniaj±c± pracê niezale¿nie od g³êbi koloru (ilo¶ci bitów na
piksel). GTK (druga czê¶æ GTK+) jest natomiast ju¿ zbiorem ró¿nego
rodzaju kontrolek s³u¿±cych do tworzenia interfejsu u¿ytkownika.

%description -l pt_BR
Bibliotecas X originalmente escritas para o GIMP, que agora estão
sendo também usadas por vários outros programas.

%description -l tr
Baþlangýçta GIMP için yazýlmýþ X kitaplýklarý. Þu anda baþka
programlarca da kullanýlmaktadýr.

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
