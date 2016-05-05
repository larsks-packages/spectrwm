Name:           spectrwm
Version:        3.0.1
Release:        3%{?dist}

# build github tag name from package name and version
%global tag_base    %{lua: print(string.upper(rpm.expand("%name")))}
%global tag_version %{lua: print((string.gsub(rpm.expand("%version"), "%.", "_")))}

Summary:        Minimalist tiling window manager written in C
License:        ISC
URL:            https://github.com/conformal/%{name}
Source0:        https://github.com/conformal/%{name}/archive/%{tag_base}_%{tag_version}.tar.gz
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXft-devel
BuildRequires:  libXt-devel
BuildRequires:  libXrandr-devel
BUildRequires:  git

# This is the default program[term]
Requires:       xterm

# This is the default program[lock]
Requires:       xlockmore

# This is the default program[menu]
Requires:       dmenu

# THis is used by the screenshot.sh script
Requires:       scrot

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
make -C linux CC="%{__cc} %{optflags} %{__global_ldflags}" \
    %{?_smp_mflags} \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    MANDIR=%{_mandir} \
    DATAROOTDIR=%{_datadir}

%install
make -C linux install CC="%{__cc} %{optflags} %{__global_ldflags}" \
    %{?_smp_mflags} \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    DATAROOTDIR=%{_datadir} \
    MANDIR=%{_mandir} \
    DESTDIR=%{buildroot}

rm -f %{buildroot}%{_bindir}/scrotwm

install -d %{buildroot}%{_sysconfdir}
install -pm 644 %{name}.conf %{buildroot}%{_sysconfdir}

install -dp %{buildroot}%{_datadir}/%{name}

for file in baraction.sh initscreen.sh screenshot.sh; do
    install $file %{buildroot}%{_datadir}/%{name}
done

for file in spectrwm_*.conf; do
    install $file %{buildroot}%{_datadir}/%{name}
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE LICENSE-LD_PRELOAD LICENSE-dwm README.md
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/xsessions/%{name}.desktop
%{_libdir}/libswmhack.so*
%{_mandir}/man1/%{name}.1.gz

%changelog
* Wed May 05 2016 Lars Kellogg-Stedman <lars@oddbit.com>
- Packaged 3.0.1
