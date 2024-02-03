%define pkgversion %(echo %version|sed "s/\\\\\./_/g")

Name: desmume
Version: 0.9.13
Release: 5%{?dist}
Summary: A Nintendo DS emulator

License: GPLv2+
URL: http://desmume.org/
Source0: https://github.com/TASEmulators/desmume/archive/release_%{pkgversion}/%{name}-%{version}.tar.gz
# Fix format strings
Patch0: %{name}-0.9.13-formatstring.patch
# Use system tinyxml instead of the embedded copy
Patch1: %{name}-0.9.13-tinyxml.patch
# Fix building on aarch64
# https://github.com/TASEmulators/desmume/issues/551
Patch2: %{name}-0.9.13-aarch64.patch
#Fix building on ppc64le
# https://github.com/TASEmulators/desmume/issues/550
Patch3: %{name}-0.9.13-ppc64le.patch
Patch4: %{name}-0.9.13-arm.patch

BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(libpcap)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(soundtouch)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(tinyxml)
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
Requires: hicolor-icon-theme

# desmume-glade is no longer provided
Provides: desmume-glade = %{version}-%{release}
Obsoletes: desmume-glade < 0.9.13


%package cli
Summary: A Nintendo DS emulator (CLI version)


%description
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.


%description cli
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

This is the CLI version.


%prep
%autosetup -p1 -n %{name}-release_%{pkgversion}

pushd desmume

# Remove bundled tinyxml
rm -rf src/utils/tinyxml

# Fix end-of-line encoding
sed -i 's/\r//' AUTHORS

# Fix file encoding
for txtfile in AUTHORS
do
    iconv --from=ISO-8859-1 --to=UTF-8 $txtfile > tmp
    touch -r $txtfile tmp
    mv tmp $txtfile
done

# Fix premissions
find src -name *.[ch]* -exec chmod 644 {} \;

popd


%build
pushd desmume/src/frontend/posix
%meson
%meson_build
popd

%install
pushd desmume/src/frontend/posix
%meson_install
popd

# Validate desktop file
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/org.desmume.DeSmuME.desktop

# Verify AppData file
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/org.desmume.DeSmuME.metainfo.xml


%files
%doc desmume/AUTHORS desmume/ChangeLog desmume/README desmume/README.LIN
%license desmume/COPYING
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/org.desmume.DeSmuME.*
%{_datadir}/applications/org.desmume.DeSmuME.desktop
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/org.desmume.DeSmuME.metainfo.xml


%files cli
%doc desmume/AUTHORS desmume/ChangeLog desmume/README desmume/README.LIN
%license desmume/COPYING
%{_bindir}/%{name}-cli
%{_mandir}/man1/%{name}-cli.1*


%changelog
* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Mon Jun 20 2022 Andrea Musuruane <musuruan@gmail.com> - 0.9.13-2
- Fixed building on ppc64le
- Fixed building on aarch64

* Sat Jun 18 2022 Andrea Musuruane <musuruan@gmail.com> - 0.9.13-1
- Updated to upstream version 0.9.13
- Spec file clean up

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.9.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.9.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 0.9.11-6
- Rebuild for soundtouch 2.0.0

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 Andrea Musuruane <musuruan@gmail.com> - 0.9.11-4
- Fixed FTBFS
- Added soundtouch-devel and libpcap-devel to BR

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 28 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.9.11-2
- fix gcc6 compile issue
- quick spec file clean up

* Thu May 14 2015 Andrea Musuruane <musuruan@gmail.com> - 0.9.11-1
- Updated to upstream version 0.9.11
- Spec file cleanup

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

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

