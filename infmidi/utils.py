from typing import Tuple, Union

import numpy as np
from matplotlib import pyplot as plt

from .core import Clip, Midi, Note, Track, item2midi

__all__ = ["plot"]

PLOT_DEFAULT_MIN_LENGTH = 4

def get_piano_roll(clip: Clip, length: int, resolution: int=64):
    # length = max(clip.length, PLOT_DEFAULT_MIN_LENGTH)
    piano_roll = np.zeros((128, int(resolution * length)))
    for note in clip.notes:
        start = int(note.location*resolution)
        end = int((note.location + note.length)*resolution)
        piano_roll[note.value, start:end-1] = note.velocity
    return piano_roll
    
def plot_midi(
    mid: Midi,
    grid_axis: str = "both",
    grid_linestyle: str = ":",
    grid_linewidth: float = 0.5,
    resolution: int = 24,
    figsize: Tuple[float] = (10, 6.18),
    **kwargs,
):

    if not mid.tracks:
        raise RuntimeError("There is no track to plot.")

    cmaps = ("Blues", "Oranges", "Greens", "Reds", "Purples", "Greys")
    n_tracks = len(mid.tracks)
    length = max([track.notes_length for track in mid.tracks] + [PLOT_DEFAULT_MIN_LENGTH])
    xticklabes = np.arange(0, length, 4**(int(length**0.25) - 1))

    if n_tracks > 1:
        fig, axs_ = plt.subplots(n_tracks, figsize=(figsize[0], figsize[1] * n_tracks), sharex=False)
        fig.subplots_adjust(hspace=0)
        axs = axs_.tolist()
    else:
        fig, ax = plt.subplots(figsize=(10, 6.18))
        axs = [ax]


    # Plot tracks
    for idx, (track, ax) in enumerate(zip(mid.tracks, axs)):
        
            piano_roll = get_piano_roll(track.clip, length, resolution)
    
            ax.imshow(
                piano_roll,
                cmap=cmaps[idx % len(cmaps)],
                aspect="auto",
                vmin=0,
                vmax=127,
                origin="lower",
                interpolation="none",
                **kwargs,
            )
            ax.tick_params(
                direction='in',
                bottom=False,
                top=False,
                left=True,
                right=False,
            )

            # Format x-axis
            ax.set_xticks(resolution * xticklabes - 0.5)
            ax.set_xticklabels("")
            # ax.tick_params(axis="x", which="major", width=0)

            # Format y-axis
            ax.set_yticks(np.arange(0, 128, 12))
            ax.set_yticklabels(["C{}".format(i - 1) for i in range(11)])

            # Format axis labels
            ax.set_ylabel(f"{track.name}\n\nnote")

            # Plot the grid
            ax.grid(
                axis=grid_axis,
                color="k",
                linestyle=grid_linestyle,
                linewidth=grid_linewidth,
            )
    else:
        ax.set_xticks(resolution * xticklabes - 0.5)
        ax.set_xticklabels(xticklabes)
        ax.set_xlabel("location (beat)")


def plot(item: Union[Note, Clip, Track, Midi], **kwargs) -> None:
    plot_midi(item2midi(item.copy(), **kwargs), **kwargs)