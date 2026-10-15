/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <string.h>

static void say_first_line(const char *path)
{
    char line[80] = {};
    FILE *file = fopen(path, "r");

    if (file == nullptr)
        return;
    if (fgets(line, sizeof(line), file) != nullptr)
        fputs(line, stdout);
    fclose(file);
}

int main(int count, char **given)
{
    char name[80] = {};

    puts("? name");
    fflush(stdout);
    if (fgets(name, sizeof(name), stdin) == nullptr)
        return 1;
    name[strcspn(name, "\n")] = '\0';
    printf("hello, %s\n", name);
    if (count > 1)
        say_first_line(given[1]);
    return 0;
}
