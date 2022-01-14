import statistics
from shared.utils import Utils

class Informer():
    """
    Send POST request to endpoint based on known user/pass field name params
    """
    def print_response_times_data(times):
        # TODO: implement full report with enhanced UI
        median = statistics.median(times)
        maxDelta = Utils.maxDelta(times)
        maxRatio = maxDelta / median
        print("\n>> Max Time Diff: {}".format(maxDelta))
        print(">> Median time:   {}".format(median))
        print(">> MaxDiff ratio: {:.2f}".format(maxRatio * 100) + "%")
        if maxRatio < 10.0:
            print("\n[!] Warning: Max Time Difference to median is too low ( < 10% ).")
            print("[!] The site may not be vulnerable or no user existed from given list.")
        report = input("\n[-] Scan done. Output full report? (y/N) ")
        if report is 'y':
            print("Report")