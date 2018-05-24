program surface
	real :: pi, r, h, v, s
	pi = 3.1415926
	print *, 'input radius r and height h ?'
	read *, r, h
	v = pi * h * r**2 / 3.0
	s = pi * r * (r + sqrt(r**2 + h**2))
	print *, 'Volume = ', v
	print *, 'Area.  = ', s
end program surface
Thu May 24 16:06:00 2018