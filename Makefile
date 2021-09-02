LED:
	# create SSB cache to avoid race conditions
	time python3 scripts/LED_check_8rounds.py 0 0
	# main run
	time parallel -j 4 -v python3 scripts/LED_check_8rounds.py ::: 0 1 2 3 ::: 0 1 2 3
	# verify
	make LED_verify

LED_verify:
	# create SSB cache to avoid race conditions
	time python3 scripts/LED_verify.py 0 0
	# stop immediately after any job fails
	time parallel -j 4 -v --halt=now,fail=1 python3 scripts/LED_verify.py ::: 0 1 2 3 ::: 0 1 2 3
	echo All verified

LED_bench:
	time parallel -j 4 time python3 scripts/LED_check_8rounds.py ::: 0 1 ::: 0 1 ::: 0 1 ::: 0 1 ::: 0 1 ::: 0 1 ::: 0 1

LED_bench_analyze:
	# create log from scratch (disabled)
	#bash -c 'cd logs; for f in *.info.log; do grep "Cons" $$f; grep SAT_times $$f | wc -l; grep "avg" $$f | tail -1; echo; done' | tee logs/timings.log
	#python3 scripts/benchmark_analyze.py logs/timings.log
	
	# saved resulting log
	python3 scripts/benchmark_analyze.py logs_benchmark/timings.log


ssb:
	python ./scripts/ssb_divcore.py SSB_ZEROKEY_LED
	python ./scripts/ssb_divcore.py SSB_ZEROKEY_SKINNY64
	python ./scripts/ssb_divcore.py SSB_SKINNY64
	python ./scripts/ssb_divcore.py SSB_LED
	python ./scripts/ssb_divcore.py SSB_MIDORI64


setup:
	pip install packages/justlogs packages/hackycpp packages/optisolveapi
	pip install packages/subsets
	pip install packages/divprop
