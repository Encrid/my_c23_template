/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <malloc.h>

#include "library.h"

void *aligned_block(void)
{
    return (_aligned_malloc(16, 16));
}

void aligned_drop(void *block)
{
    _aligned_free(block);
}
