/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "failed.h"

int said(const char *text, int status)
{
    say("%s\n", text);
    return (status);
}
