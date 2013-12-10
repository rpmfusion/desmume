%if (0%{?fedora} && 0%{?fedora}) < 19
%global with_desktop_vendor_tag 1
%endif

Name: desmume
Version: 0.9.10
Release: 1%{?dist}
Summary: A Nintendo DS emulator

License: GPLv2+
URL: http://desmume.org/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.tar
# Do not look into builddir
Patch0: %{name}-0.9-dontlookinbuilddir.patch
# Fix compile errors
# Upstream CVS
Patch1: %{name}-0.9.10-glx_3Demu.patch
# Use system tinyxml instead of the embedded copy
Patch2: %{name}-0.9.10-tinyxml.patch

BuildRequires: gtkglext-devel
BuildRequires: libglade2-devel
BuildRequires: openal-soft-devel
%if 0%{?fedora} >= 20
BuildRequires:  compat-lua-devel
%else
BuildRequires:  lua-devel
%endif
BuildRequires: zziplib-devel 
BuildRequires: agg-devel
BuildRequires: tinyxml-devel
# Not yet in Fedora
#BuildRequires: soundtouch-devel >= 1.5.0
BuildRequires: gettext
BuildRequires: intltool
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
%patch1 -p1
%patch2 -p1

# Remove bundled tinyxml
rm -rf src/utils/tinyxml

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
%configure \
  --enable-openal \
  --enable-glade
make %{?_smp_mflags}


%install
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
%if %{with_desktop_vendor_tag}
  --vendor dribble \
%endif
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install \
  --delete-original \
%if %{with_desktop_vendor_tag}  
  --vendor dribble \
%endif
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-glade.desktop

%find_lang %{name}-glade


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%post glade
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


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
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/32x32/apps/DeSmuME.xpm
%if %{with_desktop_vendor_tag} 
%{_datadir}/applications/dribble-%{name}.desktop
%else
%{_datadir}/applications/%{name}.desktop
%endif
%{_mandir}/man1/%{name}.1*
%doc AUTHORS ChangeLog COPYING README README.LIN


%files glade -f %{name}-glade.lang
%{_bindir}/%{name}-glade
%{_datadir}/%{name}-glade
%{_datadir}/icons/hicolor/32x32/apps/DeSmuME-glade.xpm
%if %{with_desktop_vendor_tag}
%{_datadir}/applications/dribble-%{name}-glade.desktop
%else
%{_datadir}/applications/%{name}-glade.desktop
%endif
%{_mandir}/man1/%{name}-glade.1*
%doc AUTHORS ChangeLog COPYING README README.LIN


%files cli
%{_bindir}/%{name}-cli
%{_mandir}/man1/%{name}-cli.1*
%doc AUTHORS ChangeLog COPYING README README.LIN


%changelog
* Sun Dec 01 2013 Andrea Musuruane <musuruan@gmail.com> - 0.9.10-1
- Updated to upstream version 0.9.10
- Added a patch to use system tinyxml
- Built with compat-lua for F20+
- Dropped cleaning at the beginning of %%install
- Updated desktop database because desmume desktop entry has MimeType key

* Wed May 01 2013 Andrea Musuruane <musuruan@gmail.com> - 0.9.9-1
- Updated to upstream version 0.9.9
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped desktop vendor tag for F19+

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.8-2
- Mass rebuilt for Fedora 19 Features

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

* Sat Sep 08 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-4
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

