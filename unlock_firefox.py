#!/usr/bin/env python

import os
import ConfigParser

base_path = os.path.expanduser(os.sep.join(['~','.mozilla','firefox']))

profile_filename = os.sep.join([base_path, 'profiles.ini'])

profile_parser = ConfigParser.ConfigParser()
profile_parser.read(profile_filename)
sections = [x for x in profile_parser.sections() if x != 'General']
for section in sections:
    if len(sections) == 1 or profile_parser.has_option(section, 'Default'):
        # this is the default section
        profile_path = profile_parser.get(section, 'path')
        if profile_parser.getboolean(section, 'isrelative'):
            profile_path = os.sep.join([base_path, profile_path])
        profile_listing = os.listdir(profile_path)
        for lockfile in ['lock', '.parentlock']:
            if lockfile in profile_listing:
                os.remove(os.sep.join([profile_path, lockfile])
        print 'Firefox is now unlocked and can be opened'
        break
