/* Examples/jerasure_03.c
 * James S. Plank

Jerasure - A C/C++ Library for a Variety of Reed-Solomon and RAID-6 Erasure Coding Techniques
Copright (C) 2007 James S. Plank

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
  
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
 
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
  
James S. Plank
Department of Electrical Engineering and Computer Science
University of Tennessee 
Knoxville, TN 37996
plank@cs.utk.edu
*/

/*
 * $Revision: 1.2 $
 * $Date: 2008/08/19 17:41:40 $
 */
    

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jerasure.h"

#define talloc(type, num) (type *) malloc(sizeof(type)*(num))

usage(char *s)
{
  fprintf(stderr, "usage: jerasure_03 k w - Creates a kxk Cauchy matrix in GF(2^w). \n\n");
  fprintf(stderr, "       k must be < 2^w.  Element i,j is 1/(i+(2^w-j-1)).  (If that is\n");
  fprintf(stderr, "       1/0, then it sets it to zero).  \n");
  fprintf(stderr, "       It then tests whether that matrix is invertible.\n");
  fprintf(stderr, "       If it is invertible, then it prints out the inverse.\n");
  fprintf(stderr, "       Finally, it prints the product of the matrix and its inverse.\n");
  fprintf(stderr, "       \n");
  fprintf(stderr, "This demonstrates: jerasure_print_matrix()\n");
  fprintf(stderr, "                   jerasure_invertible_matrix()\n");
  fprintf(stderr, "                   jerasure_invert_matrix()\n");
  fprintf(stderr, "                   jerasure_matrix_multiply().\n");
  if (s != NULL) fprintf(stderr, "%s\n", s);
  exit(1);
}

int main(int argc, char **argv)
{
  unsigned int k, w, i, j, n;
  int *matrix;
  int *matrix_copy;
  int *inverse;
  int *identity;

  if (argc != 3) usage(NULL);
  if (sscanf(argv[1], "%d", &k) == 0 || k <= 0) usage("Bad k");
  if (sscanf(argv[2], "%d", &w) == 0 || w <= 0 || w > 31) usage("Bad w");
  if (k >= (1 << w)) usage("K too big");

  matrix = talloc(int, k*k);
  matrix_copy = talloc(int, k*k);
  inverse = talloc(int, k*k);

  for (i = 0; i < k; i++) {
    for (j = 0; j < k; j++) {
      n = i ^ ((1 << w)-1-j);
      matrix[i*k+j] = (n == 0) ? 0 : galois_single_divide(1, n, w);
    }
  }

  printf("The Cauchy Matrix:\n");
  jerasure_print_matrix(matrix, k, k, w);
  memcpy(matrix_copy, matrix, sizeof(int)*k*k);
  i = jerasure_invertible_matrix(matrix_copy, k, w);
  printf("\nInvertible: %s\n", (i == 1) ? "Yes" : "No");
  if (i == 1) {
    printf("\nInverse:\n");
    memcpy(matrix_copy, matrix, sizeof(int)*k*k);
    i = jerasure_invert_matrix(matrix_copy, inverse, k, w);
    jerasure_print_matrix(inverse, k, k, w);
    identity = jerasure_matrix_multiply(inverse, matrix, k, k, k, k, w);
    printf("\nInverse times matrix (should be identity):\n");
    jerasure_print_matrix(identity, k, k, w);
  }
  return 0;
}

