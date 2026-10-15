/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

static_assert(alignof(double) >= 4);

int main(void)
{
    bool ready = true;
    const char *nothing = nullptr;

    if (!ready || nothing != nullptr)
        return 1;
    puts("hello, c23");
    return 0;
}
