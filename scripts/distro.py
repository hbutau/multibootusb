#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name:     distro.py
# Purpose:  Module to detect if distro types supported by multibootusb (by extracting specific files)
# Authors:  Sundar
# Licence:  This file is a part of multibootusb package. You can redistribute it or modify
# under the terms of GNU General Public License, v.2 or above

import os
import string
import platform
import re
from .iso import *
from .isodump3 import ISO9660
from .gen import *
from . import _7zip
from . import config


def distro(iso_cfg_ext_dir, iso_link):
    """
    Detect if distro is supported by multibootusb.
    :param iso_cfg_ext_dir: Directory where *.cfg files are extracted.
    :return: Detected distro name as string.
    """
    iso9660fs = ISO9660(iso_link)
    # iso_file_list = iso9660fs.readDir("/")
    iso_file_list = _7zip.list_iso(iso_link)
    if platform.system() == "Linux" or platform.system() == "Windows":
        for path, subdirs, files in os.walk(iso_cfg_ext_dir):
            for name in files:
                if name.endswith('.cfg') or name.endswith('.CFG') or name.endswith('.txt') or name.endswith('.TXT') \
                        or name.endswith('.lst'):
                    try:
                        # errors='ignore' is required as some files also contain non utf character
                        string = open(os.path.join(path, name),  errors='ignore').read()
                    except IOError:
                        return "Read Error."
                    else:
                        if any("f4ubcd" in s.lower() for s in iso_file_list):
                            return "f4ubcd"
                        if re.search(r'ubcd', string, re.I):
                            return "ubcd"
                        elif re.search(r'Super Grub Disk', string, re.I):
                            return "sgrubd2"
                        elif re.search(r'hbcd', string, re.I):
                            return "hbcd"
                        elif re.search(r'systemrescuecd', string, re.I):
                            return "systemrescuecd"
                        elif re.search(r'pmagic|partedmagic', string, re.I) and isolinux_bin_exist(iso_link):
                            return "parted-magic"
                        elif re.search(r'mgalive', string, re.I):  # mounting fat filesystem hard coded in to initrd.
                            # Can be modified only under linux.
                            return "mageialive"
                        elif re.search(r'archisolabel|misolabel', string, re.I):
                            return "arch"
                        elif re.search(r'chakraisolabel', string, re.I):
                            return "chakra"
                        elif re.search(r'boot=live', string, re.I) and isolinux_bin_exist(iso_link):
                            return "debian"
                        elif re.search(r'debian-installer', string, re.I) and isolinux_bin_exist(iso_link):
                            return "debian-install"
                        elif re.search(r'solydx', string, re.I):
                            return "solydx"
                        elif re.search(r'knoppix', string, re.I):
                            return "knoppix"
                        elif re.search(r'root=live:CDLABEL=', string, re.I):
                            return "fedora"
                        elif re.search(r'redhat', string, re.I):
                            return "redhat"
                        # elif re.search(r'suse', string, re.I):
                        #   return "suse"
                        elif re.search(r'opensuse', string,
                                       re.I):
                            return "opensuse"
                        elif re.search(
                                r'slitaz|dban |ophcrack|tinycore|rescue.cpi|xpud|untangle|4mlinux|partition wizard|android-x86.png|'
                                r'riplinux|lebel dummy|http://pogostick.net/~pnh/ntpasswd/|AVG Rescue CD', string, re.I):
                            return "slitaz"
                        elif re.search(r'boot=casper', string, re.I):
                            return "ubuntu"
                        elif re.search(r'wifislax', string, re.I):
                            return "wifislax"
                        elif re.search(r'slax', string, re.I):
                            return "slax"
                        elif re.search(r'sms|vector|autoexec', string, re.I) and isolinux_bin_exist(iso_link):
                            return "sms"
                        elif re.search(r'antix', string, re.I):
                            return "antix"
                        elif re.search(r'porteus', string, re.I):
                            return "porteus"
                        elif re.search(r'livecd=livecd|PCLinuxOS', string, re.I):
                            return "pclinuxos"
                        elif re.search(r'looptype=squashfs', string, re.I):
                            return "gentoo"
                        elif re.search(r'finnix', string, re.I):
                            return "finnix"
                        elif re.search(r'wifiway', string, re.I):
                            return "wifiway"
                        elif re.search(r'puppy|quirky', string, re.I):
                            return "puppy"
                        elif re.search(r'ipcop', string, re.I):
                            return "ipcop"
                        elif re.search(r'ipfire', string, re.I):
                            return "ipfire"
                        elif re.search(r'zenwalk|slack|salix', string, re.I) and re.search(r'live', string, re.I):
                            return "salix-live"
                        elif re.search(r'zenwalk|slack|salix', string, re.I):
                            return "zenwalk"
                        elif re.search(r'ubuntu server', string, re.I):
                            return "ubuntu-server"
                        elif re.search(r'Welcome to CentOS', string, re.I):
                            return "centos-net-minimal"
                        elif re.search(r'Trinity Rescue Kit', string, re.I):
                            return "trinity-rescue"
                        elif re.search(r'alpine', string, re.I):
                            return "alpine"
                        elif re.search(r'http://support.kaspersky.com', string, re.I):
                            return "kaspersky"
                        elif re.search(r'ALT Linux', string, re.I):
                            return "alt-linux"
                        elif re.search(r'Sergei Strelec', string, re.I):
                            return "Windows"
                        elif re.search(r'ReactOS', string, re.I):
                            return "ReactOS"
                        elif re.search(r'fsecure', string, re.I):
                            return "fsecure"

        distro = detect_iso_from_file_list(iso_link)
        if distro:
            return distro
            # FIXME: See the below comments.
            '''
            else:
                # FIXME: The idea of detecting as generic is to work like a unetbootin if other methods fails.
                #  This simply extracts distro to root of the USB and install syslinux on isolinux.bin directory.
                #  All works fine but unable to boot the distro successfully. Also, see the generic section from
                #  syslinux, update_cfg and install_distro modules.
                if self.isolinux_bin_exist():
                    return "generic"
            '''
        else:
            return None


def detect_iso_from_file_list(iso_link):
    """
    Fallback detection script from the content of an ISO.
    :return: supported distro as string
    """
    if os.path.exists(iso_link):
        iso_file_list = _7zip.list_iso(iso_link)
        if any("sources" in s.lower() for s in iso_file_list) and any("boot.wim" in s.lower() for s in iso_file_list):
            return "Windows"
        elif any("config.isoclient" in s.lower() for s in iso_file_list):
            return "opensuse"
        elif any("dban" in s.lower() for s in iso_file_list):
            return "slitaz"
        elif any("memtest.img" in s.lower() for s in iso_file_list):
            return "mentest"
        elif any("menu.lst" in s.lower() for s in iso_file_list):
            return "grub4dos"
        else:
            log(iso_file_list)

if __name__ == '__main__':
    iso_cfg_ext_dir = os.path.join(multibootusb_host_dir(), "iso_cfg_ext_dir")
    #iso_link = '../../../DISTROS/2016/debian-live-8.3.0-amd64-lxde-desktop.iso'
    iso_link = '/media/sundar/Data/DISTROS/ubuntu_14_04_backup/Downloads/clonezilla-live-2.4.2-32-amd64.iso'
    iso_extract_file(iso_link, iso_cfg_ext_dir, 'cfg')
    log(distro(iso_cfg_ext_dir))
