Name:       spectrwm
Version:    3.0.1

# build github tag name from package name and version
%global tag_base	%{lua: print(string.upper(rpm.expand("%name")))}
%global tag_version	%{lua: print((string.gsub(rpm.expand("%version"), "%.", "_")))}

Release:    1%{?dist}
Summary:    Minimalist tiling window manager written in C
License:    ISC
URL:        https://github.com/conformal/%{name}
Source0:    https://github.com/conformal/%{name}/archive/%{tag_base}_%{tag_version}.tar.gz
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXft-devel
BuildRequires:  libXt-devel
BuildRequires:  libXrandr-devel
BUildRequires:  git
Requires:   xterm
Requires:   xlockmore
Requires:   dmenu

# LKS: This should be picked up automatically (but it's not).
Provides: libswmhack.so.0.0()(64bit)

%description
Spectrwm is a small dynamic tiling window manager for X11.
It tries to stay out of the way so that valuable screen real
estate can be used for much more important stuff.
It has sane defaults and does not require one to learn a
language to do any configuration. It was written by hackers
for hackers and it strives to be small, compact and fast.

%prep
%autosetup -S git -n spectrwm-%{tag_base}_%{tag_version}
# Generate license files as per
# https://opensource.conformal.com/wiki/spectrwm#License
head -n14 version.h | tail -n13 | sed -e 's/ \* //g' -e 's/\*//g' > LICENSE
head -n55 spectrwm.c | tail -n30 | sed -e 's/ \* //g' -e 's/\*//g' > LICENSE-dwm
head -n38 lib/swm_hack.c | tail -n21 | sed -e 's/ \* //g' -e 's/\*//g' > LICENSE-LD_PRELOAD

%build
make CC="%{__cc} %{optflags} %{__global_ldflags}" -C linux/ %{?_smp_mflags} PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
make CC="%{__cc} %{optflags} %{__global_ldflags}" -C linux/ install PREFIX=%{_prefix} LIBDIR=%{_libdir} DESTDIR=%{buildroot}
install -d %{buildroot}%{_sysconfdir}
install -pm 644 %{name}.conf %{buildroot}%{_sysconfdir}
install -dp %{buildroot}%{_datadir}/{%{name},xsessions}
install -m 644 linux/%{name}.desktop %{buildroot}%{_datadir}/xsessions
install baraction.sh %{buildroot}%{_datadir}/%{name}
install initscreen.sh %{buildroot}%{_datadir}/%{name}
install screenshot.sh %{buildroot}%{_datadir}/%{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE LICENSE-LD_PRELOAD LICENSE-dwm README.md
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/scrotwm
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/baraction.sh
%{_datadir}/%{name}/initscreen.sh
%{_datadir}/%{name}/screenshot.sh
%{_datadir}/xsessions/%{name}.desktop
%{_libdir}/libswmhack.so*
%{_mandir}/man1/%{name}.1.gz

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.7.2-1
- Resolves: rhbz#1224438 - update to 2.7.2

* Sat Jan 31 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.6.2-1
- Resolves: rhbz#1187927 - update to 2.6.2

* Sat Jan 10 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.6.1-1
- Resolves: rhbz#1157605 - update to 2.6.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 13 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.5.1-2
- Resolves: rhbz#1095967 - own /usr/share/spectrwm (didn't go in 2.5.1-1)

* Sun Jul 13 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.5.1-1
- Resolves: rhbz#1095890 - upstream version bump to 2.5.1
- Resolves: rhbz#1095967 - spectrwm packaging issues
- generate and install appropriate licenses

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 2.5.0-1
- BZ 1071352 - upstream version bump to 2.5.0

* Tue Jan 21 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.4.0-2
- install spectrwm.desktop file

* Sat Nov 23 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.4.0-1
- version bump
- spectrwm.conf added via install step and not via patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.3.0-2
- scrotwm symlink not removed to match with upstream

* Fri May 17 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.3.0-1
- latest stable version 2.3.0

* Sat Apr 27 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-10
- prefix no longer hardcoded

* Tue Apr 16 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-9
- doc flag removed, not needed in this case

* Tue Apr 16 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-8
- post and postun removed for devel package
- doc line not left empty

* Tue Apr 16 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-7
- arch specific conditions from build and install stages removed

* Tue Apr 16 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-6
- default programs used by spectrwm mentioned as Requires

* Mon Apr 15 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-5
- shlib symlinks handled in upstream Makefile, not in spec

* Sat Apr 13 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-4
- versioned shared lib patch modified

* Fri Apr 12 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-3
- only unversioned .so file goes into devel
- url and source links don't use hardcoded package name

* Thu Apr 11 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-2
- extra blank lines removed
- hardcoded name and version removed
- scriptlets moved below install section
- man pages are in the doc section
- added default programs used to BR (xterm,xlock,dmenu)
- versioned shared library uses -Wl,-soname and goes into devel package
- symlinks .so.0 and .so to shared library created

* Mon Apr 01 2013 Lokesh Mandvekar <lsm5@buffalo.edu> 2.2.0-1
- initial package (2.2.0)
