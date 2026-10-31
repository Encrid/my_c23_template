/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#ifndef CHECKED_H
    #define CHECKED_H

    #include <stddef.h>

void *checked_copy(void *to, const void *from, size_t len);
void *checked_move(void *to, const void *from, size_t len);
void *checked_set(void *to, int fill, size_t len);
int checked_compare(const void *left, const void *right, size_t len);
size_t checked_length(const char *text);
int checked_deep(unsigned char seed);

#endif
