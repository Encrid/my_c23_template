/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <sys/mman.h>
#include <unistd.h>

#include "guard.h"

unsigned char *make_guarded(size_t len)
{
    size_t page = (size_t)sysconf(_SC_PAGESIZE);
    size_t room = (len + page - 1) / page * page;
    unsigned char *base = mmap(nullptr, room + 2 * page,
        PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (base == MAP_FAILED || mprotect(base, page, PROT_NONE)
        || mprotect(base + page + room, page, PROT_NONE))
        return (nullptr);
    return (base + page);
}
