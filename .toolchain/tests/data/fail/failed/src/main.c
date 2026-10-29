/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>

#include "failed.h"

static int opened(void)
{
    if (door_open() < 0)
        return (said("no door", 5));
    door_shut();
    return (said("a door, opened and shut", 0));
}

static int grown(void)
{
    char *zeroed = calloc(2, 4);
    char *bigger = nullptr;

    if (!zeroed)
        return (said("no zeroed block", 3));
    bigger = realloc(zeroed, 16);
    if (!bigger) {
        free(zeroed);
        return (said("no bigger block", 4));
    }
    free(bigger);
    return (opened());
}

int main(int count, [[maybe_unused]] char **words)
{
    char *one = first_block();
    char *two = nullptr;
    int done = 0;

    if (!one)
        return (said("no first block", 1));
    two = malloc(8);
    if (!two && count > 1)
        return (said("no second block, and the first is kept", 2));
    if (!two) {
        free(one);
        return (said("no second block", 2));
    }
    done = grown();
    free(two);
    free(one);
    return (done);
}
