/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdarg.h>
#include <stdio.h>

#include "failed.h"

static bool opened;

int door_open(void)
{
    opened = true;
    return (0);
}

bool door_lock(void)
{
    return (opened);
}

void door_shut(void)
{
    opened = false;
}

int say(const char *format, ...)
{
    va_list list;
    int written = 0;

    va_start(list, format);
    written = vprintf(format, list);
    va_end(list);
    return (written);
}
