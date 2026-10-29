/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "started.h"
#include "typed.h"

static unsigned long one(void *arg)
{
    return (arg != nullptr);
}

static void *two(void *arg)
{
    return (arg);
}

static int said(const char *text, int status)
{
    puts(text);
    return (status);
}

int main(void)
{
    static int held;

    if (start_one(one, &held) < 0)
        return (said("no first start", 1));
    if (start_two(two, &held) < 0)
        return (said("no second start", 2));
    if (thread_started() < 0)
        return (said("no thread", 3));
    return (said("two starts and a thread", 0));
}
