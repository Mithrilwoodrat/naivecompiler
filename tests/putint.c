extern int putchar(int c);

void putint(int n)
{
    int c;
    if (n < 0 || n > 9) {
        return ;
    }
    c = n + 48;
    putchar(c);
}

/*
int main()
{
    putint(6);
    return 0;
}*/