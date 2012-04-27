Name: desmume
Version: 0.9.8
Release: 1%{?dist}
Summary: A Nintendo DS emulator

Group: Applications/Emulators
License: GPLv2+
URL: http://desmume.org/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Do not look into builddir
Patch0: %{name}-0.9-dontlookinbuilddir.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gtkglext-devel
BuildRequires: libglade2-devel
BuildRequires: openal-soft-devel
BuildRequires: lua-devel
BuildRequires: zziplib-devel 
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: agg-devel
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme


%package glade
Summary: A Nintendo DS emulator (Glade GUI version)
Group: Applications/Emulators

%package cli
Summary: A Nintendo DS emulator (CLI version)
Group: Applications/Emulators


%description
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

%description glade
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

This is the GTK/Glade version.

%description cli
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

This is the CLI version.


%prep
%setup -q
%patch0 -p1

# Fix end-of-line encoding
sed -i 's/\r//' AUTHORS

# Fix file encoding
for txtfile in ChangeLog AUTHORS
do
    iconv --from=ISO-8859-1 --to=UTF-8 $txtfile > tmp
    touch -r $txtfile tmp
    mv tmp $txtfile
done

# Fix premissions
chmod 644 src/*.{cpp,h}
chmod 644 src/gtk-glade/*.{cpp,h}
chmod 644 src/gtk-glade/dTools/*.{cpp,h}

# Fix glade path
sed -i 's|gladedir = $(datadir)/desmume/glade|gladedir = $(datadir)/desmume-glade/|g' src/gtk-glade/Makefile.{am,in}

# We need a different icon for desmume-glade
sed -i 's|Icon=DeSmuME|Icon=DeSmuME-glade|g' src/gtk-glade/desmume-glade.desktop

# Fix gettext package name
sed -i 's|GETTEXT_PACKAGE=desmume|GETTEXT_PACKAGE=desmume-glade|g' configure{,.ac}


%build
%configure --enable-openal
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove installed icon
rm %{buildroot}%{_datadir}/pixmaps/DeSmuME.xpm

# Install icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -m 644 src/gtk/DeSmuME.xpm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
install -m 644 src/gtk/DeSmuME.xpm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/DeSmuME-glade.xpm

# Rename desktop files and fix categories
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --delete-original \
  --vendor dribble \
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install \
  --delete-original \
  --vendor dribble \
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-glade.desktop

%find_lang %{name}-glade


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%post glade
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%postun glade
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%posttrans glade
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/32x32/apps/DeSmuME.xpm
%{_datadir}/applications/dribble-%{name}.desktop
%{_mandir}/man1/%{name}.1*
%doc AUTHORS ChangeLog COPYING README README.LIN


%files glade -f %{name}-glade.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}-glade
%{_datadir}/%{name}-glade
%{_datadir}/icons/hicolor/32x32/apps/DeSmuME-glade.xpm
%{_datadir}/applications/dribble-%{name}-glade.desktop
%{_mandir}/man1/%{name}-glade.1*
%doc AUTHORS ChangeLog COPYING README README.LIN


%files cli
%defattr(-,root,root,-)
%{_bindir}/%{name}-cli
%{_mandir}/man1/%{name}-cli.1*
%doc AUTHORS ChangeLog COPYING README README.LIN


%changelog
* Thu Apr 26 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.8-1
- Updated to upstream version 0.9.8

* Sun Apr 15 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.7-5
- Fixed microphone support (BZ #2231)
- Enabled LUA engine

* Sat Mar 17 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.7-4
- Fixed FTBFS for F17+

* Sat Mar 17 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.7-3
- Fixed an error in desmume-glade.desktop (BZ #2229)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.7-2
- Rebuilt for c++ ABI breakage

* Sun Feb 06 2011 Andrea Musuruane <musuruan@gmail.com> 0.9.7-1
- Updated to upstream version 0.9.7

* Sun Jun 06 2010 Andrea Musuruane <musuruan@gmail.com> 0.9.6-1
- Updated to upstream version 0.9.6-1
- Fixed Source0 URL

* Sun Dec 06 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.5-2
- Added a patch from upstream to compile on big endian systems (SF #2909694)

* Sun Dec 06 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.5-1
- Updated to upstream version 0.9.5
- Updated icon cache scriptlets

* Fri Jul 24 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.4-1
- Updated to upstream version 0.9.4
- Added a fix to compile under gcc 4.4 (SF #2819176)
- Removed no longer needed patches
- Removed no longer needed Debian man pages
- Cosmetic changes

* Thu Apr 30 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.2-2
- Added a patch from upstream to fix IO Regs menu crash (SF #2781065)

* Sun Apr 19 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.2-1
- Updated to upstream version 0.9.2
- Removed no longer needed patch to compile with gcc 4.4
- Added a patch from upstream to compile on 64 bit systems (SF #2755952)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.1-3
- rebuild for new F11 features

* Sat Feb 14 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.1-2
- Made a patch to compile with gcc 4.4 (SF #2599049)

* Fri Feb 13 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.1-1
- Updated to upstream version 0.9.1

* Sun Jan 04 2009 Andrea Musuruane <musuruan@gmail.com> 0.9-1
- Updated to upstream version 0.9

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.8-2
- rebuild for buildsys cflags issue

* Wed Apr 23 2008 Andrea Musuruane <musuruan@gmail.com> 0.8-1
- Updated to upstream version 0.8

* Sun Sep 08 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-4
- Using debian sources because many things were missing from upstream
- Removed no longer needed automake and autoconf from BR
- Updated icon cache scriptlets to be compliant to new guidelines

* Tue Aug 21 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-3
- Added missing automake libtool to BR

* Mon Aug 20 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-2
- Added missing autoconf to BR

* Sat Aug 18 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-1
- Updated to upstream version 0.7.3
- Added man pages from Debian
- Updated License tag from GPL to GPLv2+
- Removed %%{?dist} tag from changelog

* Sun Jun 24 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.1-1
- Updated to upstream version 0.7.1
- Updated icon cache scriptlets to be compliant to new guidelines

* Thu Jun 07 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.0-2
- Added a patch from Ian Chapman to remove the buggy tools menu which 
  only contains IO regs which frequently crashes desmume on x86_64
- Added a patch from Ian Chapman to make desmume-glade ONLY look in the 
  installed location for it's .glade files and not to use the "uninstalled" 
  location
- Shortened description
- Better use of %%{name} macro

* Fri May 25 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.0-1
- Updated to upstrem version 0.7.0

* Sun Mar 25 2007 Andrea Musuruane <musuruan@gmail.com> 0.6.0-1
- Initial release for Dribble

