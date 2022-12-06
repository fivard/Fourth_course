from mido import MidiFile
import numpy as np
import pandas as pd


def read_midi_file(path):
    return MidiFile(path, clip=True)


def np_to_csv(arr, path):
    pd.DataFrame(arr).to_csv(path, index=False, header=False)


def csv_to_np_array(path):
    res = np.genfromtxt(path, delimiter=',').astype(int)

    if len(np.shape(res)) == 1:
        res = np.array([res])

    return res


def save_track_as_midi(track, path):
    track.save(path)