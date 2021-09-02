lib:
	python setup.py build -f
	cp build/lib.linux-x86_64-*/divprop/*.so src/divprop/
	#make
	# make test
	
qpy:
	bash -c 'python setup.py bdist_wheel &>/dev/null'
	python -m pip install --upgrade --no-deps --force-reinstall dist/divprop-*-cp38-cp38-linux_x86_64.whl

qsage:
	sage -sh -c 'python setup.py bdist_wheel &>/dev/null'
	sage -pip install --upgrade --no-deps --force-reinstall dist/divprop-*-cp38-cp38-linux_x86_64.whl

qpypy:
	pypy3 setup.py bdist_wheel
	pypy3 -m pip install --upgrade --no-deps --force-reinstall dist/divprop-*-pp37-pypy37_pp73-linux_x86_64.whl


test:
	python -m pytest --doctest-modules tests/ src/
	python -m pytest --doctest-modules tests_sage/
	#sage -sh -c 'pytest tests/ tests_sage/'

clean:
	rm -rf build
	rm -f src/divprop/*_wrap.cpp
	rm -f src/divprop/lib.py
	rm -f src/divprop/*.so

venv:
	sage -python -m venv --system-site-packages .envsage/
	echo `pwd`/src >.envsage/lib/python*/site-packages/divprop.pth
	ln -sf .envsage/bin/activate ./activate

