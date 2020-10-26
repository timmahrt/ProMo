'''
Created on Sep 18, 2013

@author: timmahrt
'''

import math

try:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
except ImportError:
    hasMatplotlib = False
else:
    hasMatplotlib = True

 
def _matplotlibCheck():
    if not hasMatplotlib:
        raise ImportError("Matplotlib required to generate plots. "
                          "Install matplotlib or disable plotting")


def plotSinglePitchTrack(fromTuple, fnFullPath):
    _matplotlibCheck()

    fig, (ax0) = plt.subplots(nrows=1)

    # Old data
    plot1 = ax0.plot(fromTuple, color='red', linewidth=2,
                     )

    plt.ylabel('Pitch (Hz)')
    plt.xlabel('Sample number')

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#     plt.legend([plot1, plot2, plot3], ["From", "To", "Merged line"])

    plt.savefig(fnFullPath, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plotTwoPitchTracks(fromTuple, toTuple, fnFullPath):
    _matplotlibCheck()

    fig, (ax0, ax1) = plt.subplots(nrows=2)

    # Old data
    plot1 = ax0.plot(fromTuple, color='red', linewidth=2,
                     # label="From"
                     )
    ax0.set_title("Mary is going to the mall (statement)")

    plot2 = ax1.plot(toTuple, color='red', linewidth=2,
                     # label="From"
                     )

    ax1.set_title("Mary is going to the mall (question)")

    plt.ylabel('Pitch (Hz)')
    plt.xlabel('Sample number')

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#     plt.legend([plot1, plot2, plot3], ["From", "To", "Merged line"])

    plt.savefig(fnFullPath, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plotF0(fromTuple, toTuple, mergeTupleList, fnFullPath):
    '''
    Plots the original data in a graph above the plot of the dtw'ed data
    '''
    _matplotlibCheck()

    fig, (ax0) = plt.subplots(nrows=1)

    # Old data
    plot1 = ax0.plot(fromTuple[0], fromTuple[1], color='red',
                     linewidth=2, label="From")
    plot2 = ax0.plot(toTuple[0], toTuple[1], color='blue',
                     linewidth=2, label="To")
    ax0.set_title("Plot of F0 Morph")
    plt.ylabel('Pitch (hz)')
    plt.xlabel('Time (s)')

    # Merge data
    colorValue = 0
    colorStep = 255.0 / len(mergeTupleList)
    for timeList, valueList in mergeTupleList:
        colorValue += colorStep
        hexValue = "#%02x0000" % int(255 - colorValue)
        if int(colorValue) == 255:
            ax0.plot(timeList, valueList, color=hexValue, linewidth=1,
                     label="Merged line, final iteration")
        else:
            ax0.plot(timeList, valueList, color=hexValue, linewidth=1)

    plt.legend(loc=1, borderaxespad=0.)
#     plt.legend([plot1, plot2, plot3], ["From", "To", "Merged line"])

    plt.savefig(fnFullPath, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plotIntensity(fromDataList, toDataList, mergeTupleList,
                  controlPoints, fnFullPath):

    def mag2DB(valueList):
        stepSize = 500

        returnList = []
        for i in range(int(math.ceil(len(valueList) / float(stepSize)))):
            subList = valueList[i * stepSize:(i + 1) * stepSize]
            value = math.sqrt(sum([val ** 2 for val in subList]))

            returnList.append(20.0 * math.log10(value))

        return returnList

    _matplotlibCheck()

    fromDataList = mag2DB(fromDataList)
    toDataList = mag2DB(toDataList)

    print(max(fromDataList))
    print(max(toDataList))

    fig, ax0 = plt.subplots(nrows=1)
#     fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

    # Old data
    plot1 = ax0.plot(fromDataList, color='red', linewidth=2, label="From")
#     plot1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plot2 = ax0.plot(toDataList, color='blue', linewidth=2, label="To")
#     plot2.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax0.set_title("Plot of Intensity Morph")
    plt.ylabel('RMS intensity (db)')
    plt.xlabel('Time (s)')

    # Merge data

    colorValue = 0
    colorStep = 255.0 / len(mergeTupleList)
    for valueList in mergeTupleList:

        valueList = mag2DB(valueList)

        print(max(valueList))

        colorValue += colorStep
        hexValue = "#%02x0000" % int(255 - colorValue)
        xValues = [i for i in range(len(valueList))]
        if colorValue == 255.0:
            plot3 = ax0.plot(xValues, valueList, color=hexValue, linewidth=1,
                             label="Merged line")
        else:
            plot3 = ax0.plot(xValues, valueList, color=hexValue, linewidth=1)

    controlPoints = mag2DB(controlPoints)
    xValues = [i for i in range(len(controlPoints))]
    ax0.scatter(xValues, controlPoints, color='pink', label="Control points")

    plt.legend(loc=1,
               # bbox_to_anchor=(1.05, 1), loc=2,
               borderaxespad=0.)

    plt.savefig(fnFullPath, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plotDuration(fromDurationList, toDurationList, resultDataList,
                 labelList, fnFullPath):

    _matplotlibCheck()

    dataList = [fromDurationList, ] + resultDataList + [toDurationList, ]

    # Sanity check
    for subList in dataList:
        assert(len(subList) == len(fromDurationList))

    # Constants
    colorTuple = ['red', 'yellow', 'blue']
    width = 0.2
    n = len(dataList)
    iterN = range(n)

    # Pre-plotting work
    fig, ax0 = plt.subplots(nrows=1)

    # Labels
    ax0.set_title("Plot of Duration Morph")
    plt.ylabel('Duration (s)')
    plt.xlabel('Iterations')
    plt.title('Duration morph')

    # Draw x ticks (iteration numbers)
    xLabelList = []
    for i in range(len(resultDataList)):
        xLabelList.append(str(i + 1))  # 1 based

    xLabelList = ["From", ] + xLabelList + ["To", ]
    iterN2 = [val + width / 2.0 for val in iterN]
    plt.xticks(iterN2, xLabelList)

    # Plot the data
    transposedList = zip(*dataList)
    bottom = [0 for i in iterN]
    for i, row in enumerate(transposedList):

        # Horizontal line that sits on the tallest column
        ax0.axhline(bottom[0], color="black")

        # Word label that appears after the final column
        bottomAppend = max(row)
        ax0.text(n - 1.0 + 0.5, (bottom[0] + (bottomAppend / 3.0)),
                 labelList[i])

        # The column data
        ax0.bar(x=iterN, height=row, bottom=bottom, width=width,
                alpha=0.6, color=colorTuple[i % 3])

        # Update the start positions for the next iteration

        bottom = [origBottom + bottomAppend for origBottom in bottom]

    # Draw a final horizontal line over the highest column
    ax0.axhline(bottom[0], color="black")

    # Save and cleanup
    plt.savefig(fnFullPath, dpi=300, bbox_inches='tight')
    plt.close(fig)
