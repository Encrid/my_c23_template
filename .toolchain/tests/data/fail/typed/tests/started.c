/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "started.h"

int start_one(start_fn_t start, void *arg)
{
    return ((int)start(arg));
}

int start_two(void *(*start)(void *arg), void *arg)
{
    return (start(arg) != nullptr);
}
