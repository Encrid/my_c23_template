/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <windows.h>

#include "guard.h"

unsigned char *make_guarded(size_t len)
{
    SYSTEM_INFO info;
    size_t page;
    size_t room;
    unsigned char *base;
    DWORD old;

    GetSystemInfo(&info);
    page = info.dwPageSize;
    room = (len + page - 1) / page * page;
    base = VirtualAlloc(nullptr, room + 2 * page, MEM_RESERVE | MEM_COMMIT,
        PAGE_READWRITE);
    if (!base || !VirtualProtect(base, page, PAGE_NOACCESS, &old)
        || !VirtualProtect(base + page + room, page, PAGE_NOACCESS, &old))
        return (nullptr);
    return (base + page);
}
