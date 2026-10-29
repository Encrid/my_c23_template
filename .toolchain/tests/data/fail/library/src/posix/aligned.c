/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>

#include "library.h"

void *aligned_block(void)
{
    return (aligned_alloc(16, 16));
}

void aligned_drop(void *block)
{
    free(block);
}
