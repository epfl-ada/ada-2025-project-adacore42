# General utilities
import warnings
    
def absolute_index2contest_index(absolute_idx):
    """
    Fonction to obtain the contest index (e.g. 510) from the absolute index after preprocessing.

    Inputs : absolute index of the contest, obtained from precprocessing [0; 383]
    Outputs : index of the contest as given by The New Yorker Caption Contest [510; 895]

    Exceptions :
    - Contest 525 is suppressed : offset +1 from absolute index 15
    - Contest 540 is suppressed : offset +2 from absolute index 30
    """
    if 0 <= absolute_idx < 15:
        return 510 + absolute_idx
    elif 15 <= absolute_idx < 29:
        return 510 + absolute_idx + 1
    elif 29 <= absolute_idx <= 383:
        return 510 + absolute_idx + 2
    else:
        warnings.warn(f"Absolute index {absolute_idx} is out of valid range [0; 383]. Returning None.")
        return None



def contest_index2absolute_index(contest_idx):
    """
    Fonction to obtain the absolute index [0; 383] from the contest index [510; 895].
    Inputs: contest index as given by The New Yorker Caption Contest [510; 895]
    Outputs: absolute index of the contest, obtained from preprocessing [0; 383]
    Exceptions:
    - Contest 525 is suppressed : offset +1 from absolute index 15
    - Contest 540 is suppressed : offset +2 from absolute index 30
    """
    if contest_idx < 510 or contest_idx > 895:
        warnings.warn(f"Contest index {contest_idx} is out of valid range [510; 895]. Returning None.")
        return None

    if contest_idx < 525:
        return contest_idx - 510

    elif contest_idx < 540:
        return contest_idx - 510 - 1

    else:
        return contest_idx - 510 - 2
