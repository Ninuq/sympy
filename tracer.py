import sys, trace, pytest, os, glob


def run():
    arg = sys.argv[1]
    path_to_test = os.path.split(arg)
    global file_name
    _, file_name = path_to_test
    file_name = file_name.replace("test_", "")
    path = os.path.join(os.path.dirname(__file__), *path_to_test)
    pytest.main([path, "-q"])


# Creates a tracer from the Trace module
tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=0, count=1)

# Run the given test file and collect its results
tracer.run("run()")
results = tracer.results()


# Filters out all unnecessary counters
new_counts = {}
for name, value in results.__dict__["counter"].items():
    if file_name in name[0] and not "test" in name[0]:
        new_counts[name] = value
        break

# Monkey patching the internal counts of the trace module
results.counts = new_counts

# Writes results to *.cover file.
results.write_results(show_missing=True, coverdir=".")

# Opens found file into vim
for file in glob.glob("*.cover"):
    os.system(f"vim {file}")
    break