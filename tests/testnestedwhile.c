int main()
{
  int a;
  int b;
  a = 1;
  b = 1;
  while (a < 10) {
	a = a + 1;
    while( b < 5) {
        b = b + 1;
        if (b == 3) {
            break;
        }
    }
  }
  return 0;
}
