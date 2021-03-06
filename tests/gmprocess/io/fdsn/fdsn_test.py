#!/usr/bin/env python

import os.path
from gmprocess.io.fdsn.core import read_fdsn
from gmprocess.io.test_utils import read_data_dir
from gmprocess.streamcollection import StreamCollection
from gmprocess.processing import process_streams
from numpy.testing import assert_almost_equal


def test_channel_exclusion():
    
    exclude_patterns = ['*.*.??.???']
    datafiles, origin = read_data_dir('fdsn', 'se60247871', 'US.LRAL*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 0

    exclude_patterns = ['*.*.??.LN?']
    datafiles, origin = read_data_dir('fdsn', 'se60247871', 'US.LRAL*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 0

    exclude_patterns = ['*.*.??.LN?']
    datafiles, origin = read_data_dir('fdsn', 'nc72282711', 'BK.CMB*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 3

    exclude_patterns = ['*.*.??.[BH]NZ']
    datafiles, origin = read_data_dir('fdsn', 'ci38445975', 'CI.MIKB*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 4

    exclude_patterns = ['US.*.??.???']
    datafiles, origin = read_data_dir('fdsn', 'se60247871', 'US.LRAL*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 0

    exclude_patterns = ['*.LRAL.??.???']
    datafiles, origin = read_data_dir('fdsn', 'se60247871', 'US.LRAL*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 0

    exclude_patterns = ['*.*.40.???']
    datafiles, origin = read_data_dir('fdsn', 'nc73300395', 'BK.VALB*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 0

    exclude_patterns = ['US.LRAL.20.LNZ']
    datafiles, origin = read_data_dir('fdsn', 'se60247871', 'US.LRAL*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 2

    exclude_patterns = ['*.*.??.BN?', '*.*.??.HN?']
    datafiles, origin = read_data_dir('fdsn', 'ci38445975', 'CI.MIKB*.mseed')
    streams = []
    for datafile in datafiles:
        tstreams = read_fdsn(datafile, exclude_patterns=exclude_patterns)
        if tstreams == None:
            continue
        else:
            streams += tstreams
    assert len(streams) == 0



def test_weird_sensitivity():
    datafiles, origin = read_data_dir('fdsn', 'us70008dx7', 'SL.KOGS*.mseed')
    streams = []
    for datafile in datafiles:
        streams += read_fdsn(datafile)
    sc = StreamCollection(streams)
    psc = process_streams(sc, origin)
    channel = psc[0].select(component='E')[0]
    assert_almost_equal(channel.data.max(), 62900.191900393373)


def test():
    datafiles, origin = read_data_dir('fdsn', 'nc72282711', 'BK.CMB*.mseed')
    streams = []
    for datafile in datafiles:
        streams += read_fdsn(datafile)

    assert streams[0].get_id() == 'BK.CMB.HN'

    datafiles, origin = read_data_dir('fdsn', 'nc72282711', 'TA.M04C*.mseed')
    streams = []
    for datafile in datafiles:
        streams += read_fdsn(datafile)

    assert streams[0].get_id() == 'TA.M04C.HN'

    # test assignment of Z channel
    datafiles, origin = read_data_dir('fdsn', 'nc73300395', 'BK.VALB*.mseed')
    streams = []
    for datafile in datafiles:
        streams += read_fdsn(datafile)

    # get all channel names
    channels = sorted([st[0].stats.channel for st in streams])
    assert channels == ['HN2', 'HN3', 'HNZ']

    # DEBUGGING
    sc = StreamCollection(streams)
    psc = process_streams(sc, origin)


if __name__ == '__main__':
    os.environ['CALLED_FROM_PYTEST'] = 'True'
    test_channel_exclusion()
    test_weird_sensitivity()
    test()
