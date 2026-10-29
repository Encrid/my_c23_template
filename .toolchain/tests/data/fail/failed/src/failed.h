/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#ifndef FAILED_H
    #define FAILED_H

void *first_block(void);
int said(const char *text, int status);
int door_open(void);
bool door_lock(void);
void door_shut(void);
int say(const char *format, ...);

#endif
