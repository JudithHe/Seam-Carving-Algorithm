Seam-Carving-Algorithm
======================
I have written a program in python to implement Seam Carving algorithm using Dynamic Programming.

The program takes an image as an input, reads it using pylabs imread and gets a ndarray.
Algorithm for Seam Carving:
1.	Read the image, get the matrix representation of the image with RGB values.
2.	Calculate the gradient of the image using sobel filters.
3.	Construct a cost matrix:
a.	Initialize cost matrix=sOfIJ=Energy Gradient matrix.
b.	for i in range (0 to rows):
c.	           for j in range(0 to columns):
d.	                sOfIJ[i,j]= sOfIJ[i,j]+min(sOfIJ[i+1,j-1], sOfIJ[i+1,j] ,sOfIJ[i+1,j+1])
e.	Calculate min element from the last row and get its index.
4.	Take the sOfIJ i.e cost matrix, take the index of min element and start backtracking the seam from bottom to top.
5.	Plot the seam while backtracking and remove it to resize the image.
	
The algorithm is based on a dynamic programming approach. It is very optimal approach compared to Djakstra’s shortest path algorithm.
The running time of my algorithm is O(rows*columns).
