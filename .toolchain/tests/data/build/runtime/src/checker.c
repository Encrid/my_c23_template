/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <string.h>

#include "checked.h"
#include "guard.h"

constexpr size_t ROOM = 8192;

static unsigned char *place(unsigned char *base, size_t len, int right)
{
    return (right ? base + ROOM - len : base);
}

static int check_copy(unsigned char *a, unsigned char *b, size_t len, int right)
{
    unsigned char *to = place(a, len, right);
    unsigned char *from = place(b, len, !right);
    int bad = 0;

    for (size_t i = 0; i < len; i++)
        from[i] = (unsigned char)(i * 7 + len);
    checked_copy(to, from, len);
    for (size_t i = 0; i < len; i++)
        bad += to[i] != from[i];
    checked_set(to, (int)(len + 0x1a5), len);
    for (size_t i = 0; i < len; i++)
        bad += to[i] != (unsigned char)(len + 0x1a5);
    return (bad != 0);
}

static int check_move(unsigned char *a, size_t len, size_t to_at, size_t from_at)
{
    unsigned char *base = place(a, len + 16, 1);
    unsigned char want[8192];
    int bad = 0;

    for (size_t i = 0; i < len + 16; i++)
        base[i] = (unsigned char)(i * 11 + 3);
    for (size_t i = 0; i < len; i++)
        want[i] = base[from_at + i];
    checked_move(base + to_at, base + from_at, len);
    for (size_t i = 0; i < len; i++)
        bad += base[to_at + i] != want[i];
    return (bad != 0);
}

static int check_text(unsigned char *a, unsigned char *b, size_t len)
{
    unsigned char *left = place(a, len + 1, 1);
    unsigned char *right = place(b, len + 1, 1);
    int bad = 0;

    for (size_t i = 0; i < len; i++)
        left[i] = right[i] = (unsigned char)(1 + i % 200);
    left[len] = right[len] = 0;
    bad += checked_length((const char *)left) != len;
    bad += checked_compare(left, right, len + 1) != 0;
    if (len)
        right[len - 1]++;
    bad += len && checked_compare(left, right, len + 1) >= 0;
    return (bad != 0);
}

static int check_sizes(unsigned char *a, unsigned char *b)
{
    static const size_t big[] = { 511, 512, 513, 1000, 4096, 8176 };
    int bad = 0;

    for (size_t len = 0; len < 300 + sizeof(big) / sizeof(big[0]); len++) {
        size_t n = len < 300 ? len : big[len - 300];

        bad += check_copy(a, b, n, 0) + check_copy(a, b, n, 1);
        bad += check_move(a, n, 0, 16) + check_move(a, n, 16, 0);
        bad += check_move(a, n, 3, 11) + check_move(a, n, 11, 3);
        bad += check_text(a, b, n);
    }
    return (bad);
}

int main(int argc, char **argv)
{
    unsigned char *a = make_guarded(ROOM);
    unsigned char *b = make_guarded(ROOM);
    int bad = 0;

    if (!a || !b)
        return (2);
    bad += check_sizes(a, b);
    bad += checked_deep(7) != 15;
    if (argc > 1 && !strcmp(argv[1], "wrong"))
        bad++;
    printf("bad %d\n", bad);
    return (0);
}
