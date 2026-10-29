/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <errno.h>
#include <pthread.h>

#include "typed.h"

static void *run(void *arg)
{
    return (arg);
}

int thread_started(void)
{
    static int held;
    pthread_t thread;

    if (pthread_create(&thread, nullptr, run, &held))
        return (-1);
    pthread_join(thread, nullptr);
    return (0);
}
