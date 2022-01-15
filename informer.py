import statistics
from colors import Colors
from shared.utils import Utils

class Informer():
    def __init__(self, averageTimes):
        self.times = averageTimes

    """
    Preliminar report with overall data
    """
    def print_response_times_data(self, times):
        # TODO: implement full report with enhanced UI
        median = statistics.median(times)
        maxDelta = Utils.maxDelta(times)
        maxRatio = maxDelta / median
        print("\n>> Max Time Diff:    {:.6f}".format(maxDelta))
        print(">> Aggregate Median: {:.6f}".format(median))
        # print(">> MaxDiff ratio: {:.2f}".format(maxRatio * 100) + "%")
        if maxRatio < 10.0:
            print(Colors.WARNING)
            print("\n[!] Warning: Max Time Difference to median is too low ( < 10% ).")
            print("[!] The site may not be vulnerable or no user existed from given list.\033[00m")
        report = input("\n[-] Scan done. Output full report? (y/N) \n")
        if report == 'y' or report == 'Y':
            self.print_per_user_data(median)
            
    """
    Exhaustive per-user data
    """
    def print_per_user_data(self, median):
        for user in self.times:
            av_time = self.times[user]
            deviation_ratio = av_time / median
            user_stats = "{:15}".format(user)
            deviation_stats = "{:9.2f}".format(deviation_ratio)
            if deviation_ratio >= 100:
                self.color_print(Colors.FAIL, user_stats, deviation_stats)
            elif deviation_ratio < 100 and deviation_ratio >= 20:
                self.color_print(Colors.WARNING, user_stats, deviation_stats)
            elif deviation_ratio < 20 and deviation_ratio >= 5:
                self.color_print(Colors.OKGREEN, user_stats, deviation_stats)
            elif deviation_ratio < 5 and deviation_ratio >= 1:
                self.color_print(Colors.BGREEN, user_stats, deviation_stats)
            else:
                self.color_print(Colors.OKCYAN, user_stats, deviation_stats)
    
    """
    Verbose output based on ASCII color codes
    """        
    def color_print(self, COLOR, user_stats, deviation_stats):
        print("| User: " + COLOR + user_stats + "\033[00m | Deviation: " + COLOR + deviation_stats + "\033[00m |")