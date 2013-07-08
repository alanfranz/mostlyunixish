#!/usr/bin/env python

# print all installed kernel/headers/etc BUT the current and the latest;
# suitable to be used with apt-get remove.
# requires aptitude to be installed. Works on Ubuntu and probably Debian

from subprocess import check_output
import re

def runcmd(s):
    return check_output(s.split())

# should work for anything until kernel 3.100
kernel_version_pattern = re.compile("[23]\.\d{1,2}\.\d{1,2}-\d{1,3}")
def get_kernel_version(kernelstring):
    return kernel_version_pattern.search(kernelstring).group(0)

def get_providing_packages(pkg):
    return filter(lambda x: x != "", 
        map(str.strip, 
            runcmd('aptitude search ~i~P%s -F%%p' % pkg).split("\n")
            )
        )

def get_nonmatching_packages(package_list, excluding):
    return [k for k in package_list if not get_kernel_version(k) in
        excluding]


all_kernels = get_providing_packages("linux-image")
all_kernels.sort() # lexicographical

kernel_versions = map(get_kernel_version, all_kernels)
latest_version = kernel_versions[-1]
current_version = get_kernel_version(runcmd("uname -r"))

kernels_to_remove = get_nonmatching_packages(all_kernels, (current_version,
    latest_version))

impl_headers = get_providing_packages("linux-headers")

headers_to_remove = get_nonmatching_packages(impl_headers, (current_version,
    latest_version))

# This seems to be needed in Ubuntu >= 13.04
#base_headers_to_remove = [header.replace("-generic", "") for header in headers_to_remove]
#headers_to_remove += base_headers_to_remove

print " ".join(kernels_to_remove + headers_to_remove)
