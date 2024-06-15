from concurrent.futures import ThreadPoolExecutor


def run_parallel(*args):
    with ThreadPoolExecutor(max_workers=len(args)) as executor:
        features = [executor.submit(arg) for arg in args]
        return [feature.result() for feature in features]

