/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "library.h"

static int order(const void *one, const void *two)
{
    return (*(const int *)one - *(const int *)two);
}

static int said(const char *text, int status)
{
    puts(text);
    return (status);
}

static int searched(void)
{
    static const int sorted[] = {1, 2, 3};
    const int key = 2;

    if (!memchr("ab", 'b', 2))
        return (said("no byte", 2));
    if (!bsearch(&key, sorted, 3, sizeof(sorted[0]), order))
        return (said("no key", 3));
    return (0);
}

int main(void)
{
    char byte = 0;
    void *block = nullptr;
    int done = 0;

    if (fread(&byte, 1, 1, stdin) != 1)
        return (said("no read", 1));
    done = searched();
    if (done)
        return (done);
    block = aligned_block();
    if (!block)
        return (said("no aligned block", 4));
    aligned_drop(block);
    return (said("each call gave its value", 0));
}
