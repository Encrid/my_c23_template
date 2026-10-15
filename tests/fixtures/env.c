/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>

int main(int count, char **given)
{
    const char *value = count > 1 ? getenv(given[1]) : nullptr;

    puts(value != nullptr ? value : "unset");
    return 0;
}
