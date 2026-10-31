/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <string.h>

#include "checked.h"

void *checked_copy(void *to, const void *from, size_t len)
{
    return (memcpy(to, from, len));
}

void *checked_move(void *to, const void *from, size_t len)
{
    return (memmove(to, from, len));
}

void *checked_set(void *to, int fill, size_t len)
{
    return (memset(to, fill, len));
}

int checked_compare(const void *left, const void *right, size_t len)
{
    return (memcmp(left, right, len));
}

size_t checked_length(const char *text)
{
    return (strlen(text));
}

int checked_deep(unsigned char seed)
{
    volatile unsigned char big[65536];

    for (size_t i = 0; i < sizeof(big); i += 4096)
        big[i] = seed;
    big[sizeof(big) - 1] = seed;
    return (big[sizeof(big) - 1] + big[0] + 1);
}
